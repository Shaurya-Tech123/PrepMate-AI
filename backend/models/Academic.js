const mongoose = require("mongoose");

const academicSchema = new mongoose.Schema(
  {
    studentId: { type: String, required: true, trim: true, index: true },
    attendance: { type: Number, required: true, min: 0, max: 100 },
    averageMarks: { type: Number, required: true, min: 0, max: 100 },
    failedSubjects: { type: Number, required: true, min: 0, validate: Number.isInteger },
    subjectAttempts: { type: Number, required: true, min: 0, validate: Number.isInteger },
    feeStatus: { type: String, required: true, enum: ["paid", "pending", "partial"] },
    semester: { type: Number, min: 1, max: 12, validate: Number.isInteger },
    recordedAt: { type: Date, default: Date.now }
  },
  { collection: "academic" }
);

module.exports = mongoose.model("Academic", academicSchema);
