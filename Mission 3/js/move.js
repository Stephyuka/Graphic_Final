$( document ).ready(function() {
  //Variables
  var animationTime = 1.2;

  // define 

  var tlShadow = new TimelineMax({repeat:-1});
  tlShadow.set('#shadow_1', {transformOrigin:'50% 10%', scaleX:1.26})
  .to('#shadow_1', animationTime / 2, {scaleX:1})
  .to('#shadow_1', animationTime / 2, {scaleX:1.26});
  
  var tlLegMov = new TimelineMax({repeat:-1});
  tlLegMov.set('#leg', {transformOrigin:'50% 50%'})
  .to('#leg', animationTime / 2, {rotation:1})
  .to('#leg', animationTime / 2, {rotation:1});

  var tlBodyRot = new TimelineMax({repeat:-1});
  tlBodyRot.set('#body', {transformOrigin:'50% 50%'})
  .to('#body', animationTime / 2, {rotation:8})
  .to('#body', animationTime / 2, {rotation:8});


   var tlLegLeftTrans = new TimelineMax({repeat:-1});
  tlLegLeftTrans.set('#leg-r', {y: 0})
  .to('#leg-r', animationTime / 4, {y: -25})
  .to('#leg-r', animationTime / 4, {y: -10})
  .to('#leg-r', animationTime / 2, {y: 0})


  var tlLegLeftRot = new TimelineMax({repeat:-1});
  tlLegLeftRot.set('mouth', {y: 0})
  .to('#mouth', animationTime / 2, {y:5})
  .to('#mouth', animationTime / 2, {y:0});

  var tlLegLeftRot = new TimelineMax({repeat:-1});
  tlLegLeftRot.set('#leg-r', {transformOrigin:'50% 10%', rotation:-5})
  .to('#leg-r', animationTime / 2, {rotation:-5})
  .to('#leg-r', animationTime / 2, {rotation:5});


  var tlLegRightRot = new TimelineMax({repeat:-1});
  tlLegRightRot.set('#leg-l', {transformOrigin:'50% 10%', rotation:5})
  .to('#leg-l', animationTime / 2, {rotation:5})
  .to('#leg-l', animationTime / 2, {rotation:-5});
  
  var tlLegRightTrans = new TimelineMax({repeat:-1});
  tlLegRightTrans.set('#leg-l', {y: -10})
  .to('#leg-l', animationTime / 2, {y: 5})
  .to('#leg-l', animationTime / 4, {y: -25})
  .to('#leg-l', animationTime / 4, {y: -10});

  var tlArmRight = new TimelineMax({repeat:-1});
  tlArmRight.set('#arm_r', {transformOrigin:'50% 50%', rotation:0})
  .to('#arm-r', animationTime / 2, {rotation:35})
  .to('#arm-r', animationTime / 2, {rotation:-35});
  
  var tlArmLeft = new TimelineMax({repeat:-1});
  tlArmLeft.set('#arm_l', {transformOrigin:'50% -10%', rotation:0})
  .to('#arm-l', animationTime / 2, {rotation:-15})
  .to('#arm-l', animationTime / 2, {rotation:30});




  var tlEyeLeftMov = new TimelineMax({repeat:-1});
  tlEyeLeftMov.set('#eye-left-e',{transformOrigin:'10% 40%'})
  .to('#eye-left-e', animationTime / 3, {rotation:16})
  .to('#eye-left-e', animationTime / 3, {rotation:16});

  var tlEyeRightMov = new TimelineMax({repeat:-1});
  tlEyeRightMov.set('#eye-left-e',{transformOrigin:'50% 40%'})
  .to('#eye-right-e', animationTime / 3, {rotation:8})
  .to('#eye-right-e', animationTime / 3, {rotation:8});


  //Head Animation
  var tlHeadY = new TimelineMax({repeat:-1});
  tlHeadY.to('#head', animationTime / 4, {y:'-=10'})
  .to('#head', animationTime / 4, {y:'+=10'});
  
  var tlHeadRot = new TimelineMax({repeat:-1});
  tlHeadRot.set('#head', {transformOrigin:'100% 10%'})
  .to('#head', animationTime / 2, {rotation:'-=3'})
  .to('#head', animationTime / 2, {rotation:'+=3'});
  
  //Eyebrow Animation
  var tlEyebrows = new TimelineMax({repeat:-1});
  tlEyebrows.to('.eyebrow', animationTime / 4, {y:'-=4'})
  .to('.eyebrow', animationTime / 4, {y:'+=4'});
  
  var tlEyebrowL = new TimelineMax({repeat:-1});
  tlEyebrowL.set('#eyebrow_l', {transformOrigin:'50% 50%'})
  .to('#eyebrow_l', animationTime / 4, {rotation:'-=5'})
  .to('#eyebrow_l', animationTime / 4, {rotation:'+=5'});
  
  var tlEyebrowR = new TimelineMax({repeat:-1});
  tlEyebrowR.set('#eyebrow_r', {transformOrigin:'50% 50%'})
  .to('#eyebrow_r', animationTime / 4, {rotation:'+=5'})
  .to('#eyebrow_r', animationTime / 4, {rotation:'-=5'});

});