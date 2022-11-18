const express=require("express");
var router=express.Router();
const services=require('../services/render');
const controller=require('../server/controller/cont');
const User_db=require('../connect_db')
var bcrypt=require('bcryptjs')
const fs = require("fs");
var sv_un=(req,res,next)=>{
    if(req.session.sv_un){
        next();
    }else{
        res.redirect('/login')
    }
}
router.get('/',(req,res)=>{
    console.log(req.session);
    console.log(req.sessionID)
    res.render('base',{title:"Login System"})
})
router.get('/predict',(req,res)=>{
    res.render('predict')
})

router.post('/register',async(req,res)=>{
     const {email,password}=req.body;
     let user =await User_db.findOne({email})
     if(user){
         return res.redirect('/')
     }
    else{
    const hashpw=await bcrypt.hash(password,12)
    user=new User_db({
    email,
    password:hashpw
   })
   await user.save();
   res.redirect('/login')}
})

  
router.get('/login',(req,res)=>{
    res.render('login')
})

router.post('/login',async(req,res)=>{
    const {email,password}=req.body;
    const user=await User_db.findOne({email})
    if(!user){
        return res.redirect('/')
    }
    const ismatch=await bcrypt.compare(password,user.password)
    if(!ismatch){
        return res.redirect('/login');
    }
    req.session.sv_un=true;
    req.session.user=req.body.email;
    res.redirect('/dashboard')
})
router.get('/logout',(req,res)=>{
    req.session.destroy(function(err){
        if(err){
            res.send("Sorry error found");
        }
        else{
            res.render('base',{logout:"Successfully logged out"})
        }
    })
})
router.get('/dashboard',sv_un,services.homeR);
