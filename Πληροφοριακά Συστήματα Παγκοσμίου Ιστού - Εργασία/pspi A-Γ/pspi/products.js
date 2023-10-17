const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE

    //Assigns event handlers to searchButton and submitButton
    const searchButton=document.getElementById("search")
    searchButton.onclick=searchButtonOnClick
    const sumbitButton=document.getElementById("save")
    sumbitButton.onclick=productFormOnSubmit


    // END CODE HERE
}

//This function is an event handler of the search button
searchButtonOnClick = () => {
    // BEGIN CODE HERE
    
    
        const getname = document.getElementById("inputProduct");//retrieve the field input value
        var table=document.getElementById("restable");//retrieve the table
        const res = new XMLHttpRequest();
        var rows = table.getElementsByTagName('tr');//retrieve the rows of the table
        var rowcount = rows.length;//count the rows of the table

        for (var x=rowcount-1; x>0; x--) {
          table.removeChild(rows[x]);
        }

        

        //Open a Get request
        res.open("GET", `${api}/search?name=${encodeURIComponent(getname.value)}`, true);
        
        res.onreadystatechange = () => {
          //when the response is received and has a status of 200
          if (res.readyState == 4) {
            if (res.status == 200) {
              const data = JSON.parse(res.responseText); // the response is parsed into json and passed to the data variable
              console.log(data);//log the data to the console for confirmation
             
            
              //create rows in the table and pass the data to each cell
            data.forEach(function (object){
                var tr = document.createElement('tr');
                tr.innerHTML = '<td>' + object._id + '</td>' +
                '<td>' + object.name + '</td>' +
                '<td>' + object.production_year + '</td>' +
                '<td>' + object.price + '</td>' +
                '<td>' + object.color + '</td>' +
                '<td>' + object.size + '</td>';
                table.appendChild(tr);
                
            });
            }
          }
        };

      
        res.send();
      
        
    // END CODE HERE
}

//This function is an event handler of the submit button
productFormOnSubmit = (event) => {
    // BEGIN CODE HERE

    //get the input values ​​from the form
    const res=new XMLHttpRequest();
    const getname2=document.getElementById("name");
    const getpyear=document.getElementById("pyear");
    const getcolor=document.getElementById("color");
    const getprice=document.getElementById("price");
    const getsize=document.getElementById("size");
    //Open a POST request
    res.open("POST","http://127.0.0.1:5000/add-product")
  
    res.onreadystatechange = () => {
        if (res.readyState == 4) {
            if (res.status == 200) {
                var data = JSON.parse(res.responseText);
                console.log(data);
            }
            }
            };
    res.setRequestHeader("Content-Type", "application/json;charset=UTF-8");// Define Content-type in application/json
    alert("OK")

    //sending the post request with the input prices
    res.send(JSON.stringify({
        "name": getname2.value,
        "production_year":getpyear.value,
        "price":getprice.value,
        "color":getcolor.value,
        "size":getsize.value


        }));
        //cleanup of entry after submission
        getname2.value="";
        getpyear.value="";
        getcolor.value="";
        getprice.value="";
        getsize.value="";
    
    
     

    // END CODE HERE
}