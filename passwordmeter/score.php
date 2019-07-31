<?php session_start(); ?>
<?php

if (isset($_POST["pwd_param"])){
    $param = $_POST["pwd_param"];
    $arg = $param;
    $command = escapeshellcmd('/usr/bin/python2.7 ./PSE/pwd_score_estimator.py '.$arg . " " .session_id());
    $result = exec($command,$output);
}

echo $result;
?>
