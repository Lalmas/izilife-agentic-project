<?php
error_reporting(E_ALL);
$names = ['saint-valentin.webp','epiphanie.jpg','nouvel-an.jpg','noel.jpg'];
$folder = __DIR__.'/izilife-celebration-optimized';
if ($argv[1] === 'optimize') {
    if (!is_dir($folder)) mkdir($folder, 0777, true);
    foreach ($names as $name) {
        $source = 'C:/Users/alcamara/Downloads/'.$name;
        $image = imagecreatefromstring(file_get_contents($source));
        $scale = min(1, 1400/max(imagesx($image),imagesy($image)));
        $image = imagescale($image, (int)round(imagesx($image)*$scale), (int)round(imagesy($image)*$scale), IMG_BICUBIC_FIXED);
        $dest = $folder.'/'.$name;
        if (str_ends_with($name,'.webp')) {
            imagewebp($image,$dest,80);
            if (filesize($dest)>filesize($source)) copy($source,$dest);
        } else {
            imageinterlace($image,true);
            imagejpeg($image,$dest,80);
        }
        $size=getimagesize($dest);
        echo $name,' ',$size[0],'x',$size[1],' ',filesize($source),' -> ',filesize($dest),PHP_EOL;
    }
    exit;
}
require getcwd().'/app/ThirdParty/aws/aws-autoloader.php';
$config=[];
foreach (file('.env', FILE_IGNORE_NEW_LINES) as $line) {
    if (preg_match('/^\s*(IZILIFE_AWS_\w+)\s*=\s*(.*?)\s*$/',$line,$m)) $config[$m[1]]=trim($m[2], "'\"");
}
$cred=new Aws\Credentials\Credentials($config['IZILIFE_AWS_ACCESS_KEY_ID'],$config['IZILIFE_AWS_SECRET_ACCESS_KEY']);
$signer=new Aws\Signature\S3SignatureV4('s3','eu-west-3');
function request($bucket,$method,$key='',$query=[],$body='',$headers=[]){
    global $cred,$signer;
    $url='https://'.$bucket.'.s3.eu-west-3.amazonaws.com/'.implode('/',array_map('rawurlencode',explode('/',$key)));
    if ($query) $url.='?'.http_build_query($query,'','&',PHP_QUERY_RFC3986);
    $request=$signer->signRequest(new GuzzleHttp\Psr7\Request($method,$url,$headers,$body),$cred);
    $http=curl_init($url);
    $lines=[];
    foreach ($request->getHeaders() as $n=>$values) $lines[]=$n.': '.implode(',',$values);
    curl_setopt_array($http,[CURLOPT_CUSTOMREQUEST=>$method,CURLOPT_RETURNTRANSFER=>true,CURLOPT_HTTPHEADER=>$lines,CURLOPT_TIMEOUT=>35]);
    if ($method==='PUT') curl_setopt($http,CURLOPT_POSTFIELDS,$body);
    $response=curl_exec($http);
    $status=curl_getinfo($http,CURLINFO_HTTP_CODE);
    $error=curl_error($http);
    curl_close($http);
    if ($status<200||$status>=300) {
        $xml=@simplexml_load_string((string)$response);
        throw new RuntimeException("$method $bucket/$key HTTP $status ".($xml ? (string)$xml->Code : $error));
    }
    return $response;
}
function listing($bucket,$prefix){
    $keys=[];$q=['list-type'=>'2','prefix'=>$prefix];
    do {
        $xml=simplexml_load_string(request($bucket,'GET','',$q));
        foreach ($xml->Contents as $item) $keys[(string)$item->Key]=[(int)$item->Size,(string)$item->ETag];
        $q['continuation-token']=(string)$xml->NextContinuationToken;
    } while ($q['continuation-token']!=='');
    return $keys;
}
$buckets=['izilife-dev-bucket','izilife-statging','izilifebucket'];
$prefix='statics/campains/celebrations/';
$inventories=[];
foreach ($buckets as $bucket) {
    try {
        $inventories[$bucket]=listing($bucket,$prefix);
        echo $bucket,' ',json_encode($inventories[$bucket],JSON_UNESCAPED_SLASHES),PHP_EOL;
    } catch (RuntimeException $e) {
        echo $e->getMessage(),PHP_EOL;
    }
}
if ($argv[1]!=='upload') exit;
if (count($inventories)!==3) exit(2);
$dev=$buckets[0];
foreach ($names as $name) {
    $body=file_get_contents($folder.'/'.$name);
    request($dev,'PUT',$prefix.$name,[],$body,['Content-Type'=>str_ends_with($name,'.webp')?'image/webp':'image/jpeg','Content-MD5'=>base64_encode(md5($body,true))]);
    if (request($dev,'GET',$prefix.$name)!==$body) throw new RuntimeException("Verification dev: $name");
    echo "Uploaded $dev/$prefix$name",PHP_EOL;
}
$source=listing($dev,$prefix);
foreach (array_slice($buckets,1) as $bucket) {
    foreach ($source as $key=>$identity) {
        if (($inventories[$bucket][$key]??null)===$identity) continue;
        $copySource='/'.$dev.'/'.implode('/',array_map('rawurlencode',explode('/',$key)));
        $result=simplexml_load_string(request($bucket,'PUT',$key,[],'',['x-amz-copy-source'=>$copySource]));
        if ($result->getName()!=='CopyObjectResult') throw new RuntimeException("Copy failure: $bucket/$key");
        echo "Copied $bucket/$key",PHP_EOL;
    }
    $target=listing($bucket,$prefix);
    foreach ($source as $key=>$identity) {
        if (($target[$key][0]??null)!==$identity[0]) throw new RuntimeException("Verification: $bucket/$key");
        if (in_array(substr($key,strlen($prefix)),$names,true) && request($bucket,'GET',$key)!==file_get_contents($folder.'/'.basename($key))) throw new RuntimeException("Content verification: $bucket/$key");
    }
    echo 'Verified ',$bucket,' ',count($source),' source objects',PHP_EOL;
}
