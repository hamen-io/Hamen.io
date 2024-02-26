<?php

namespace Hamen\Core\Environment;

class EnvironmentalVariables
{
    public string $filePath;
    public string $fileContents;
    public array $envVariables;

    public function __construct($filePath)
    {
        $this->filePath = $filePath;
        $this->fileContents = file_get_contents($filePath);
        $this->envVariables = [];

        $matchVars = "/((CONST|LET)\s+(INT|STR|BOOL)\s*>>\s*((?<!\\)(?:\\\\)*\"(?:[^\"\\]|\\.)*?\")\s*>>\s*((?<!\\)(?:\\\\)*\"(?:[^\"\\]|\\.)*?\"));/";

        // Execute the regular expression
        preg_match_all($matchVars, $this->fileContents, $matches);

        // Iterate over matches
        foreach ($matches[0] as $match) {
            // Extract variable details
            preg_match("/(CONST|LET)\s+(INT|STR|BOOL)\s*>>\s*((?<!\\)(?:\\\\)*\"(?:[^\"\\]|\\.)*?\")\s*>>\s*((?<!\\)(?:\\\\)*\"(?:[^\"\\]|\\.)*?\")/", $match, $varDetails);
            $scope = $varDetails[1];
            $type = $varDetails[2];
            $name = $varDetails[3];
            $value = $varDetails[4];

            // Create EnvironmentalVariable instance and add to array
            $envVar = new EnvironmentalVariable($name, $value, $type, $scope);
            if ($envVar->ok) {
                $this->envVariables[$envVar->name] = $envVar;
            }
        }
    }
}

class EnvironmentalVariable
{
    public string $name;
    public string $value;
    public string $type;
    public string $scope;
    public bool $ok;

    public function __construct($varName, $varValue, $varType, $varScope)
    {
        $this->name = $varName;
        $this->value = $varValue;
        $this->type = $varType;
        $this->scope = $varScope;

        // Ensure value and name conforms to /^".*"$/
        if (str_starts_with($this->value, "\"") && str_ends_with($this->value, "\"")) {
            $this->ok = false;
        } else if (str_starts_with($this->name, "\"") && str_ends_with($this->name, "\"")) {
            $this->ok = false;
        }

        // Validate type
        else if (!in_array($varType, ["INT", "STR", "BOOL"])) {
            $this->ok = false;
        }

        // Validate scope
        else if (!in_array($varScope, ["CONST", "LET"])) {
            $this->ok = false;
        }

        // No problems occurred
        else if ($this->ok == true) {
            // Remove leading & trailing '"' from name and value
            $this->value = substr($varValue, 1, -1);
            $this->name = substr($varName, 1, -1);

            // Parse value based on type
            switch ($varType) {
                case "INT":
                    $this->value = floatval($this->value);
                    $this->ok = $this->value != false;
                    break;
                case "STR":
                    $this->value = $this->value;
                    break;
                case "BOOL":
                    $this->value = strtoupper($this->value) == "TRUE" ? true : false;
                    break;
                default:
                    $this->ok = false;
            }
        }
    }
}

/**
 * Returns a Hamen Environmental variable
 */
function getEnv($key): EnvironmentalVariable
{
    return allEnv()->envVariables[$key];
}

/**
 * Sets the value of a given Environmental Variable
 */
function setEnv($key, $value): void
{
    throw "NOT YET";
}

/**
 * Returns a list of all Hamen Environmental variables
 */
function allEnv(): EnvironmentalVariables
{
    return new EnvironmentalVariables(__DIR__ . "/Environment");
}
