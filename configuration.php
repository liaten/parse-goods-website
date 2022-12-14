<?php
    $servername = "localhost";
    $username = "liaten";
    $password = "SECRET";
    $dbname = "wp";
    $con = new mysqli($servername, $username, $password, $dbname);
    $con->set_charset("utf8");
    
    if (!$con){
    echo 'Не могу соединиться с БД. Код ошибки: ' . mysqli_connect_errno() . ', ошибка: ' . mysqli_connect_error();
    exit;
    }
?>
