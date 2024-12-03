<?php
if(isset($_POST['hello']))
{
    session_start();
    $_SESSION = $_POST;
    if(!empty($_SESSION['name']))
    {
        $name = $_SESSION['name'];
        $protocol = (isset($_SESSION['protocol']) && !preg_match('/http|file/i', $_SESSION['protocol'])) ? $_SESSION['protocol'] : null;
        $options = (isset($_SESSION['options']) && !preg_match('/http|file|\\\/i', $_SESSION['options'])) ? $_SESSION['options'] : null;
        
        try {
            if(isset($options) && isset($protocol))
            {
                $context = stream_context_create(json_decode($options, true));
                $resp = @fopen("$protocol://127.0.0.1:3000/$name", 'r', false, $context);
            }
            else
            {
                $resp = @fopen("http://127.0.0.1:3000/$name", 'r', false);
            }

            if($resp)
            {
                $content = stream_get_contents($resp);
                echo "<div class='greeting-output'>" . htmlspecialchars($content) . "</div>";
                fclose($resp);
            }
            else
            {
                throw new Exception("Unable to connect to the service.");
            }
        } catch (Exception $e) {
            error_log("Error: " . $e->getMessage());
            
            echo "<div class='greeting-output error'>Something went wrong!</div>";
        }
    }
}
?>


<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Greetings</title>
    
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&family=Roboto&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="container text-center mt-5 animate__animated animate__fadeInDown">
    <h1 class="title">Welcome to the <span class="highlight">Greetings</span> App</h1>
    <img src="logo.png" alt="Greetings Logo" class="logo">
    <form method="POST" class="mt-4">
        <input class="form-control input-field mb-3" name="name" placeholder="Enter your name" />
        <button class="btn btn-primary submit-btn" type="submit" name="hello">
            Say Hello <i class="fas fa-smile"></i>
        </button>
    </form>
    
</div>    
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>


