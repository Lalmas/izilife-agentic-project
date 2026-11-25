<?php
declare(strict_types=1);

$envLines=file('C:/xampp/htdocs/izilife-admin/.env',FILE_IGNORE_NEW_LINES)?:[];$token='';
foreach($envLines as $line)if(preg_match('/^\s*AGENT_SECRET_TOKEN\s*=/',(string)$line)){$token=trim(substr((string)$line,strpos((string)$line,'=')+1)," \t\n\r\0\x0B\"'");break;}
if($token==='')throw new RuntimeException('AGENT_SECRET_TOKEN absent.');
$base='https://www.izilife.co/izilife-admin/';
function api2(string $route,array $payload):array{global$token,$base;$ch=curl_init($base.$route);curl_setopt_array($ch,[CURLOPT_POST=>true,CURLOPT_RETURNTRANSFER=>true,CURLOPT_HTTPHEADER=>['Content-Type: application/json','X-Agent-Token: '.$token],CURLOPT_POSTFIELDS=>json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),CURLOPT_TIMEOUT=>180,CURLOPT_CONNECTTIMEOUT=>20]);$body=curl_exec($ch);$status=(int)curl_getinfo($ch,CURLINFO_RESPONSE_CODE);$error=curl_error($ch);curl_close($ch);if($body===false||$status<200||$status>=300)throw new RuntimeException("HTTP $status $route: ".($error?:mb_substr((string)$body,0,500)));$decoded=json_decode((string)$body,true);if(!is_array($decoded)||empty($decoded['success']))throw new RuntimeException("Réponse invalide $route");return$decoded;}
function out(string $s):void{echo'['.date('H:i:s')."] $s\n";flush();}

$files=glob(__DIR__.'/../outputs/prod_experience_enrichment_*.json')?:[];usort($files,fn($a,$b)=>filemtime($b)<=>filemtime($a));
$previous=json_decode((string)file_get_contents($files[0]??''),true);$errors=(array)($previous['errors']??[]);
$report=['started_at'=>date(DATE_ATOM),'retried'=>[],'errors'=>[]];
foreach($errors as $row){$tmpId=(int)($row['tmp_id']??0);$xpId=(int)($row['experience_id']??0);if($tmpId<1)continue;try{out("Réanalyse TMP #$tmpId / XP #$xpId");$analysis=api2('scraper/agentAnalyzeExperienceTmp',['tmp_id'=>$tmpId,'source_text'=>'']);$proposal=(array)($analysis['proposal']??[]);$xp=(array)($proposal['experience']??[]);
        if(array_key_exists('experience_booking_needed_for_access_string_id',$xp)){$xp['experience_booking_needed_for_access']=$xp['experience_booking_needed_for_access_string_id'];unset($xp['experience_booking_needed_for_access_string_id']);}
        elseif(isset($xp['experience_booking_needed_for_access'])&&(is_bool($xp['experience_booking_needed_for_access'])||is_numeric($xp['experience_booking_needed_for_access'])))unset($xp['experience_booking_needed_for_access']);
        $proposal['experience']=$xp;$apply=api2('scraper/agentApplyExperienceValidation',['tmp_id'=>$tmpId,'proposal'=>$proposal,'validate'=>true,'activate'=>true]);$valid=(bool)($apply['validation']['validated']??false);$report['retried'][]=['tmp_id'=>$tmpId,'experience_id'=>$xpId,'validated'=>$valid,'blockers'=>$apply['blockers']??[]];out("TMP #$tmpId: ".($valid?'validée':'bloquée'));
    }catch(Throwable$e){$report['errors'][]=['tmp_id'=>$tmpId,'experience_id'=>$xpId,'error'=>$e->getMessage()];out("Erreur TMP #$tmpId: ".$e->getMessage());}}
$report['finished_at']=date(DATE_ATOM);$report['summary']=['retried'=>count($report['retried']),'validated'=>count(array_filter($report['retried'],fn($r)=>$r['validated'])),'blocked'=>count(array_filter($report['retried'],fn($r)=>!$r['validated'])),'errors'=>count($report['errors'])];
file_put_contents(__DIR__.'/../outputs/prod_experience_enrichment_retry_'.date('Ymd_His').'.json',json_encode($report,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));echo json_encode($report['summary'],JSON_UNESCAPED_UNICODE),"\n";
