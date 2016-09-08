'use strict';
const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname + '')));

app.get('/', function(req, res){
  res.sendFile(path.join(__dirname + '/index.html'));
});

app.get('/:filename', function(req, res){
  let mimetype;
  if(filename.match(/\.js$/)){mimetype = 'text/javascript'};
  if(filename.match(/\.css$/)){mimetype = 'text/css'};
  res.header('Content-Type', mimetype)
  res.sendFile(path.join(__dirname + '/' + filename));
});

app.listen( process.env.PORT || 8003, function(){
  console.log('Server Running');
});
