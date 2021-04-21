import mongoose from 'mongoose'

const Schema = mongoose.Schema;

const topicSchema = new Schema({
    originalPoster: {type: String, required: true},
    topicText: {type: String, required: true, minlength: 25},
    datePosted: {type: Date, required: true},
    proPosts: {type: Number, required: true},
    conPosts: {type: Number, required: true}
},
{
    timestamps: true,
});

const Topic = mongoose.model('Topic',topicSchema);

export default Topic;
