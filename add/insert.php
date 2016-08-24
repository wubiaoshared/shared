<!DOCTYPE html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8">
        <title>添加页面</title>
		
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">

        <!-- CSS -->
        <link rel="stylesheet" href="assets/css/reset.css">
        
        <link rel="stylesheet" href="assets/css/style.css">

        <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
        <!--[if lt IE 9]>
            <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->

    </head>

	<body>

	<div class="page-container">

		<?php
		header("content-type:text/html;charset=utf-8");
		date_default_timezone_set("Asia/Shanghai");
		//print_r($_POST);

		@$domain=$_POST['domain'];
		@$date=$_POST['date'];

		if($domain&&$date){
			$i=stripos($domain, ".");
			$tld=substr($domain, $i);
			
			if($tld==".in"||$tld==".co.in"){
				$link = mysql_connect('127.0.0.1', 'root', 'wb123456') 
				or die('Could not connect: ' . mysql_error());

				mysql_select_db('name') or die('Could not select database');

				// 执行 SQL 查询
				$query='select * from domain where domain="'.$domain.'" and '.'date="'.$date.'"';
				//$query='select * from domain';
				//echo $query;
				$result = mysql_query($query) or die('Query failed: ' . mysql_error());
				$ay=mysql_fetch_array($result);
				if($ay){
					echo "<h1 class='red'>".$domain."已经被人添加"."</h1>";
					
				}else{
					$addtime=date("Y-m-d H:i:s",time());
					$query = 'insert into domain(domain,date,addtime)  values("'.$domain.'","'.$date.'","'.$addtime.'")';
					//echo $query;
					$result = mysql_query($query) or die('Query failed: ' . mysql_error());
					if($result){
						echo "<h1 class='green'>".$domain."添加成功"."</h1>";
					}
					
				}


				mysql_close($link);
			}else{
				echo "<h1 class='red'>".$domain."不支持此域名后缀"."</h1>";
			}
			

		}else{
			echo "<h1 class='red'>"."域名时间都是必填项"."</h1>";
		}

		echo "<h1>"."....2秒后跳回添加页面"."</h1>";
		echo "<script>
		 setTimeout(function(){
		       window.location.href='/reg/index.html';
		 },2000)

		</script>";



		?>
			
	           
	</div>

	
	</body>


	</html>


