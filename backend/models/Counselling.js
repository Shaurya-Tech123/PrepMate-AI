const mongoose = require("mongoose");

const counsellingSchema = new mongoose.Schema(
  {
    studentId: { type: String, required: true, trim: true, index: true },
    mentorId: { type: String, required: true, trim: true, index: true },
    sessionType: { type: String, required: true, trim: true },
    status: {
      type: String,
      required: true,
      enum: ["scheduled", "completed", "cancelled", "rescheduled"]
    },
    scheduledAt: { type: Date, required: true },
    discussionTopics: { type: [String], default: [] },
    notes: { type: String, trim: true },
    followUpRequired: { type: Boolean, required: true, default: false },
    createdAt: { type: Date, default: Date.now }
  },
  { collection: "counselling" }
);

module.exports = mongoose.model("Counselling", counsellingSchema);
