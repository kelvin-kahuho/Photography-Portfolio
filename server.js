const express = require('express');
const app = express();
const path = require('path');

//Serve static files
app.use(express.static(path.join(__dirname, 'public')));

//Define routes
app.get('/', (req, res) => {
    //Serve the home.html file
    res.sendFile(path.join(__dirname, 'public/home.html'));
});

//start server
const port = 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});