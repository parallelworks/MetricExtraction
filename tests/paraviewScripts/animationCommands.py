RenderAllViews()
anim = GetAnimationScene()
anim.PlayMode = 'Snap To TimeSteps'
anim.PlayMode = 'Sequence'
>>> anim.PlayMode = 'Snap To TimeSteps'
>>> anim.AnimationTime
0.10000000149011612
>>> anim.AnimationTime = 0.2
>>> RenderAllViews()
>>> anim.AnimationTime = 0.3
>>> anim.AnimationTime = 0.2
>>> anim.AnimationTime = 0.2
>>> anim.AnimationTime = 0.3
>>> anim.PlayMode = 'Sequence'
>>> anim.AnimationTime
0.3
>>> TimeSteps
[0.10000000149011612, 0.20000000298023224, 0.30000001192092896, 0.4000000059604645, 0.5]
>>> anim.AnimationTime = TimeSteps[1]
>>> anim.AnimationTime = TimeSteps[2]
>>> 
