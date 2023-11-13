<?php

function evaluateType($type, $options, $search = "ARRAY") {
    $type = $type || "";
    $type = explode("|", $type);
    for ($i=0; $i < strlen($type); $i++) { 
        $term = $type[$i];

        if ($search === "ARRAY") {
            if (!in_array($term, $options)) return false;
        } else if ($search === "REGEX") {

        }
    }

    return true;
}

$type = $_GET["type"]; assert(evaluateType($type, ["GUIDE", "BLOG"]));
$author = $_GET["author"]; assert(evaluateType($type, "/^[_a-zA-Z]+$/", "REGEX"));

?>