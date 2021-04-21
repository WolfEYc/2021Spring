import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import topicsRouter from './routes/topics.js'
import usersRouter from './routes/users.js'
import postsRouter from './routes/posts.js'

const ATLAS_URI = 'mongodb+srv://wolfey:Pickles148@wolf.cee4u.mongodb.net/myFirstDatabase?retryWrites=true&w=majority';

const app = express();
const port = process.env.PORT || 5000;

app.use(express.json());

app.use('/topics', topicsRouter);
app.use('/users',usersRouter);
app.use('/topics/posts',postsRouter);

const uri = ATLAS_URI;
mongoose.connect(uri, {useNewUrlParser: true, useCreateIndex: true , useUnifiedTopology: true});

const connection = mongoose.connection;
connection.once('open',() =>{
    console.log("MongoDB database connection established successfully");
});



app.listen(port , () => {
    console.log(`Server is running on port: ${port}`);
});

