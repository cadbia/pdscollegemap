const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors({
  origin: 'https://pdscollegemap.herokuapp.com',
  credentials: true,
}));

// your routes go here

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
