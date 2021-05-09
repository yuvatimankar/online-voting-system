from django.contrib.auth.models import User
from django.db import models



class Poll(models.Model):
    owner    = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title     = models.CharField(max_length=255)
    pub_date = models.DateField()
    
    def __str__(self):
        return self.title

  #  This will restrict user from voting more than 
    def user_can_vote(self, user):

    #returns False if user has already voted, else True
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

#candidate model which is a child model of Poll modle 
class Candidate(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    candidate_name = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

#returning the form entries
    def __str__(self):
        return"{} = {}".format(self.poll.title[:25], self.candidate_name[:25], sef.candidate_img)


class Vote(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    poll   = models.ForeignKey(Poll, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
