<?php session_start(); ?>
<?php
function write_ini_file($assoc_arr, $path, $has_sections=FALSE) { 
    $content = ""; 
    if ($has_sections) { 
        foreach ($assoc_arr as $key=>$elem) { 
            $content .= "[".$key."]\n"; 
            foreach ($elem as $key2=>$elem2) { 
                if(is_array($elem2)) 
                { 
                    for($i=0;$i<count($elem2);$i++) 
                    { 
                        $content .= $key2."[] = \"".$elem2[$i]."\"\n"; 
                    } 
                } 
                else if($elem2=="") $content .= $key2." = \n"; 
                else $content .= $key2." = \"".$elem2."\"\n"; 
            } 
        } 
    } 
    else { 
        foreach ($assoc_arr as $key=>$elem) { 
            if(is_array($elem)) 
            { 
                for($i=0;$i<count($elem);$i++) 
                { 
                    $content .= $key."[] = \"".$elem[$i]."\"\n"; 
                } 
            } 
            else if($elem=="") $content .= $key." = \n"; 
            else $content .= $key." = \"".$elem."\"\n"; 
        } 
    } 

    if (!$handle = fopen($path, 'w')) { 
        return false; 
    }
    
    $success = fwrite($handle, $content);
    fclose($handle); 

    return $success; 
}

function write_user_training_data($path, $value){
$fp = fopen($path, 'w');
if($fp){
    fwrite($fp, $value);
}
fclose($fp);

}

if (isset($_POST["ugh"])){
    $ugh = $_POST["ugh"];
}
if (isset($_POST["ogh"])){
    $ogh = $_POST["ogh"];
}
if (isset($_POST["scoreLevelDic"])){
    $scoreLevelDic = $_POST["scoreLevelDic"];
}
if (isset($_POST["scoreLevelBF"])){
    $scoreLevelBF = $_POST["scoreLevelBF"];
}
if (isset($_POST["scoreLevelAM"])){
    $scoreLevelAM = $_POST["scoreLevelAM"];
}
if (isset($_POST["scoreLevelHS"])){
    $scoreLevelHS = $_POST["scoreLevelHS"];
}
if (isset($_POST["scoreStrengthBFN"])){
    $scoreStrengthBFN = $_POST["scoreStrengthBFN"];
}
if (isset($_POST["scoreStrengthBFNOGMAX"])){
    $scoreStrengthBFNOGMAX = $_POST["scoreStrengthBFNOGMAX"];
}
if (isset($_POST["scoreStrengthBFTMAX"])){
    $scoreStrengthBFTMAX = $_POST["scoreStrengthBFTMAX"];
}
if (isset($_POST["scoreStrengthAMMAX"])){
    $scoreStrengthAMMAX = $_POST["scoreStrengthAMMAX"];
}

if (isset($_POST["areaDicValue"])){
    $areaDicValue = $_POST["areaDicValue"];
    $path = "./PSE/user_config/user_data_trivial_".session_id().".txt";
    write_user_training_data ($path,$areaDicValue);
}

if (isset($_POST["areaAMValue"])){
    $areaAMValue = $_POST["areaAMValue"];
    $path = "./PSE/user_config/user_data_adaptive_".session_id().".txt";
    write_user_training_data ($path,$areaAMValue);
}

if (isset($_POST["areaHSValue"])){
    $areaHSValue = $_POST["areaHSValue"];
    $path = "./PSE/user_config/user_data_higherstruct_".session_id().".txt";
    write_user_training_data ($path,$areaHSValue);
}


$var = 0.3;
$sampleData = array(
                'pm_config' => array(
                    'ugh' => $ugh,
                    'ogh' => $ogh,
                    'scoreLevelDic' => $scoreLevelDic,
                    'scoreLevelBF' => $scoreLevelBF,
                    'scoreLevelAM' => $scoreLevelAM,
                    'scoreLevelHS' => $scoreLevelHS,
                    'scoreStrengthBFN' => $scoreStrengthBFN,
                    'scoreStrengthBFNOGMAX' => $scoreStrengthBFNOGMAX,
                    'scoreStrengthBFTMAX' => $scoreStrengthBFTMAX,
                    'scoreStrengthAMMAX' => $scoreStrengthAMMAX,
                ));
write_ini_file($sampleData, './PSE/user_config/config_'.session_id().'.ini', true);

//// Parse with sections
//$ini_array = parse_ini_file("./PSE/user_config/config_".session_id().".ini", true);
//print_r($ini_array);


?>
