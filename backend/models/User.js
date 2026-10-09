const mongoose = require("mongoose");

const userSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    email: { type: String, required: true, unique: true, lowercase: true, trim: true },
    role: { type: String, required: true, enum: ["student", "mentor", "admin"] },
    isActive: { type: Boolean, required: true, default: true },
    studentId: { type: String, trim: true },
    mentorId: { type: String, trim: true }
  },
  { timestamps: { createdAt: "createdAt", updatedAt: "updatedAt" }, collection: "users" }
);

module.exports = mongoose.model("User", userSchema);
