const mongoose = require("mongoose");

const subjectRecordSchema = new mongoose.Schema(
  {
    studentId: { type: String, required: true, trim: true, index: true },
    semester: { type: Number, required: true, min: 1, max: 12, validate: Number.isInteger },
    academicYear: { type: String, required: true, trim: true },
    subjectCode: { type: String, required: true, trim: true },
    subjectName: { type: String, required: true, trim: true },
    attendance: { type: Number, required: true, min: 0, max: 100 },
    totalClasses: { type: Number, required: true, min: 0, validate: Number.isInteger },
    attendedClasses: { type: Number, required: true, min: 0, validate: Number.isInteger },
    marksObtained: { type: Number, required: true, min: 0 },
    maximumMarks: { type: Number, required: true, min: 0 },
    attempts: { type: Number, required: true, min: 0, validate: Number.isInteger },
    result: { type: String, required: true, enum: ["pass", "fail", "pending"] }
  },
  { collection: "subject_records" }
);

subjectRecordSchema.pre("validate", function (next) {
  if (this.attendedClasses > this.totalClasses) {
    this.invalidate("attendedClasses", "attendedClasses cannot exceed totalClasses");
  }
  if (this.marksObtained > this.maximumMarks) {
    this.invalidate("marksObtained", "marksObtained cannot exceed maximumMarks");
  }
  next();
});

module.exports = mongoose.model("SubjectRecord", subjectRecordSchema);
