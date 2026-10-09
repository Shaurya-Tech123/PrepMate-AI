const mongoose = require("mongoose");

const applicationSchema = new mongoose.Schema(
  {
    company: { type: String, trim: true },
    role: { type: String, trim: true },
    status: { type: String, trim: true },
    appliedAt: { type: Date }
  },
  { _id: false, strict: false }
);

const placementSchema = new mongoose.Schema(
  {
    studentId: { type: String, required: true, trim: true, index: true },
    skills: { type: [String], required: true, default: [] },
    resumeStatus: {
      type: String,
      required: true,
      enum: ["not_uploaded", "uploaded", "reviewed"]
    },
    mockInterview: {
      completed: { type: Boolean, required: true, default: false },
      score: { type: Number, min: 0, max: 100, default: null }
    },
    applications: { type: [applicationSchema], default: [] },
    skillGap: {
      targetRole: { type: String, trim: true },
      missingSkills: { type: [String], default: [] }
    },
    createdAt: { type: Date, default: Date.now }
  },
  { collection: "placement" }
);

module.exports = mongoose.model("Placement", placementSchema);
