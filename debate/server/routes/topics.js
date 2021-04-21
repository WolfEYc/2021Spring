import express from 'express'
import Topic from '../models/topic.model.js';

const Router = express.Router();

Router.route('/').get((req,res)=>{
    Topic.find()
    .then(topics => res.json(topics))
    .catch(err => res.status(400).json('Error: '+err));

});

Router.route('/add').post((req,res)=>{
    const OP = req.body.originalPoster;
    const topicText = req.body.topicText;
    const date = Date.parse(req.body.datePosted);
    const proPosts = 0;
    const conPosts = 0;

    const newTopic = new Topic({
        OP,
        topicText,
        date,
        proPosts,
        conPosts
    });

    newTopic.save()
    .then(()=>res.json('User added!'))
    .catch(err => res.status(400).json('Error: '+err));
});

export default Router;