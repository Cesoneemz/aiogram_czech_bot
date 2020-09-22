<?php 

	if(isset($_POST['submit']) and $_FILES) {
		move_uploaded_file($_FILES['file']['tmp_name'], "uploades/".$_FILES['file']['name']);
		
		echo "The file has been uploaded...";
	} else echo "Error";

?>

<form method="post" action="" enctype="multipart/form-data">
<input type="file" name="file"><br>
<input type="submit" name="submit" value="Upload">
