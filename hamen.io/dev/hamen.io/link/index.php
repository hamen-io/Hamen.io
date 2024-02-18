<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

var_dump($_ENV);

require_once __DIR__ . "/../../lib/Core/Firebase/Firebase.php";
use function Hamen\Core\Firebase\instantiateFirebase;

if (!isset($_GET["url"])) {
    http_response_code(400);
    die("Error: No input URL provided.");
}

$requestedURL = $_GET["url"];
$requestedURLHost = parse_url($requestedURL);

if (!isset($requestedURLHost) || !isset($requestedURLHost["host"])) {
    http_response_code(400);
    die("Error: Bad URL.");
}

$requestedURLHost = $requestedURLHost["host"];

// Remove "www" subdomain
if (str_starts_with($requestedURLHost, "www.")) {
    $requestedURLHost = substr($requestedURLHost, strlen("www."));
}

// Ensure that the URL is a `hamen.io` host
$allowedHosts = array("hamen.io", "projects.hamen.io");
if (in_array($requestedURLHost, $allowedHosts)) {

    $shortLinkID = bin2hex(openssl_random_pseudo_bytes(4));

    $fb = instantiateFirebase();
    if (!isset($fb) || !$fb->ok()) {
        http_response_code(500);
        die("Error: Could not define database");
    }

    $fb->set($requestedURL, "SHORT_LINKS", "links", $shortLinkID);

    die();
}

http_response_code(400);
die("Error: An unknown error occurred");