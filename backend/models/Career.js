const mongoose = require("mongoose");

const recommendationSchema = new mongoose.Schema(
  {
    career: { type: String, required: true, trim: true },
    matchScore: { type: Number, required: true, min: 0, max: 100 }
  },
  { _id: false }
);

const careerSchema = new mongoose.Schema(
  {
    studentId: { type: String, required: true, trim: true, index: true },
    assessment: {
      interests: { type: [String], default: [] },
      aptitudeScore: { type: Number, min: 0, max: 100 },
      preferredDomain: { type: String, trim: true }
    },
    recommendations: { type: [recommendationSchema], default: [] },
    createdAt: { type: Date, default: Date.now }
  },
  { collection: "career" }
);

module.exports = mongoose.model("Career", careerSchema);
