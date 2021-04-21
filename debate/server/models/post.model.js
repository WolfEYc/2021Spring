import mongoose from 'mongoose'

const Schema = mongoose.Schema;

const postSchema = new Schema({
    topicID: {type: String, required: true},
    originalPoster: {type: String, required: true},
    postText: {type: String, required: true, minlength: 2},
    datePosted: {type: Date, required: true},
    proOrCon: {type: Boolean, required: true},
    Likes: {type: Number, required: true}
},
{
    timestamps: true,
})

const Post = mongoose.model('Post',postSchema);

export default Post;

