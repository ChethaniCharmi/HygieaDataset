<?php
	$email = $_POST['email'];
	$password = $_POST['password'];

	//Databse connection
	$con = new mysqli("localhost","root","Ch@rmi444","test");
	if ($con->connect_error) {
		die("Failed to connect : " .$con->connect_error);
	} else{
		$statement = $con->prepare("select * from user where email = ?");
		$statement->bind_param("s",$email);
		$statement->execute();

		$statement_result = $statement->get_result();
		if ($statement_result->num_rows > 0){
			$data = $statement_result->fetch_assoc();
			if ($data['pwd']=== $password){
				
				$message = "Login Successfully";
				echo "<script>alert('$message');</script>";
				echo "<script>window.location.href = 'prediction.html';</script>";
				//header('Location: loginSuccessModel.html');
			} else {
			$message = "Invalid Email or Password";
				echo "<script>alert('$message');</script>";
				echo "<script>window.location.href = 'login.html';</script>";
		}

		} else {
			$message = "Invalid Email or Password";
				echo "<script>alert('$message');</script>";
				echo "<script>window.location.href = 'login.html';</script>";
		}
	} 

 ?>