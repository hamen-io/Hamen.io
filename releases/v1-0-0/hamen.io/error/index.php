<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Error <?php echo $_GET["error"] ?? "404" ?> &bull; Hamen.io</title>

        <link rel="stylesheet" href="https://www.hamen.io/static/styles/index.css">
        <script type="text/javascript" src="https://www.hamen.io/static/scripts/Components.js"></script>
        <script type="text/javascript" src="https://www.hamen.io/static/scripts/index.js"></script>

        <!-- Favicon: -->
        <link rel="icon" href="https://www.hamen.io/static/media/favicon/favicon.ico" />
    </head>
    <body>
        <header></header>
        <main class="homepage">
            <section id="introduction">
                <h1 class="page-title">Error <?php echo $_GET["error"] ?? "404" ?>;</h1>
                <p><?php echo $_GET["description"] ?? "The page you are looking for does not exist!"?></p>
                <a href="https://www.hamen.io/">
                  <button type="submit" style="width: fit-content;">
                    Go Home
                  </button>
                </a>
            </section>
            <footer></footer>
        </main>
    </body>
</html>