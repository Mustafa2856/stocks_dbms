

/* javaScript Validation for SignUp / Register Page  */

    function validate(){ 
    var username = document.getElementById("username").value;
    var password = document.getElementById('password').value;
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var mobile = document.getElementById('mobile').value;
    var dob = document.getElementById('dob').value;
    var panno = document.getElementById('panno').value;
    var aadhar = document.getElementById('aadhar').value;
    var error_msg = document.getElementById("error_msg");
    error_msg.style.padding="10px";
    var text;
    
    if( username.length < 4){
        text = "Please enter username of atleast length 5";
        error_msg.innerHTML = text ;
        document.getElementById('username').focus();
        return false;
    }
    if( password.length < 6 ){
        text = "Please enter password of atleast length 7";
        error_msg.innerHTML = text ;
        document.getElementById('password').focus();
        return false;
    }
    if( name.length < 3){
        text = "Please Enter Your Full Name As per PAN Card";
        error_msg.innerHTML = text ;
        document.getElementById('name').focus();
        return false;
    }

    if( email.indexOf("@")==-1 || email.length<9 || email.indexOf(".")==-1 || email.indexOf(".")-email.indexOf("@")<2){
        text = "Please Enter Your Valid Email ID";
        error_msg.innerHTML = text ;
        document.getElementById('email').focus();
        return false;
    }
    if( mobile.length != 10 || isNaN(mobile)){
        text = "Please Enter  Valid 10 Digit Mobile Number";
        error_msg.innerHTML = text ;
        document.getElementById('mobile').focus();
        return false;
    }
    if(   !/[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}$/.test(panno) ){
        text = "Please Enter  Valid PAN Card Number";
        error_msg.innerHTML = text ;
        document.getElementById('panno').focus();
        return false;
    }
    if( aadhar.length != 12 || isNaN(aadhar)){
        text = "Please Enter  Valid 12 Digit Aadhar Card Number";
        error_msg.innerHTML = text ;
        document.getElementById('aadhar').focus();
        return false;
    }
   return true;
}

