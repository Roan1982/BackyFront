<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $titulo = htmlspecialchars($_POST['titulo']);
    $historia = htmlspecialchars($_POST['historia']);
    $autor = htmlspecialchars($_POST['autor']);
    $edad = htmlspecialchars($_POST['edad']);

    $nuevaHistoria = "Título: " . $titulo . "\n" . "Historia: " . $historia . "\n" . "Autor: " . $autor . ", Edad: " . $edad . "\n\n";

    $file = 'historias.txt';
    file_put_contents($file, $nuevaHistoria, FILE_APPEND);

    header("Location: index.html");
    exit();
}
?>
