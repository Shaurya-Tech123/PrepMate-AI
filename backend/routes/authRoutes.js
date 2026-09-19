const express=require('express');
const router=express.Router();
const {registerUser,loginUser,logout}=require("../controllers/authController")