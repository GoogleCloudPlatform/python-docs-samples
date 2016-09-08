const express = require('express');
const path = require('path');
const app = express();

app.get('/', function(req, res){
  res.send('This is the Express server');
});

app.get('/hello', function(req, res){
  res.send('Express says hello!');
});

app.listen( process.env.PORT || 8002, function(){
  console.log('Server Running');
});
