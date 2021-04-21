import express from 'express'
import Post from '../models/post.model.js';

const Router = express.Router();

Router.route('/').get((req,res)=>{
    Post.find()
    .then(topics => res.json(topics))
    .catch(err => res.status(400).json('Error: '+err));

});

Router.route('/add').post((req,res)=>{
    const topicID = req.body.topicID;
    const OP = req.body.originalPoster;
    const postText = req.body.postText;
    const date = Date.parse(req.body.datePosted);
    const proOrCon = Boolean(req.body.proOrCon);
    const Likes = Number(req.body.Likes);

    const newPost = new Post({
        topicID,
        OP,
        postText,
        date,
        proOrCon,
        Likes
    });

    newPost.save()
    .then(()=>res.json('User added!'))
    .catch(err => res.status(400).json('Error: '+err));
});

export default Router;