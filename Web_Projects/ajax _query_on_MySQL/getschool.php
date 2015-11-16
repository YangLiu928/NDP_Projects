<!DOCTYPE html>
<html>
<head>
<style>
table {
    width: 100%;
    border-collapse: collapse;
}

table, td, th {
    border: 1px solid black;
    padding: 5px;
}

th {text-align: left;}
</style>
</head>
<body>

<?php
$name = $_GET['name'];

$con = mysqli_connect('localhost','root','890928','test');
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

mysqli_select_db($con,"test");
$sql="SELECT * FROM schools WHERE name = '".$name."'"; 
// -- WHERE name = '
// ".$q.";
$result = mysqli_query($con,$sql);

echo "<table>
<tr>
<th>name</th>
<th>state</th>
<th>description</th>
</tr>";
while($row = mysqli_fetch_array($result)) {
    echo "<tr>";
    echo "<td><a data-dismiss='modal' href='#' class='description_page'>" . $row['name'] . "</a></td>";
    echo "<td>" . $row['state'] . "</td>";
    echo "<td>" . $row['description'] . "</td>";
    echo "</tr>";
}
echo "</table>";
mysqli_close($con);
?>

</body>
</html>