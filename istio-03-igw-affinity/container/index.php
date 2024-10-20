<?php
if (!isset($_SESSION['count'])) {
    session_start();		
    $_SESSION['count'] = 1;
} else {
    $_SESSION['count']++;
}
echo "Hostname: ".gethostname()."<br>\n";
echo $_SESSION['count']."th time access.\n";
?>
