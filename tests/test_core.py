import unittest
import numpy as np
from src.core import *
from src.experiment import train

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.map=dict(seed=0,start=[1.,1.],goal=[8.,1.],theta=0.,obstacles=[[5.,8.,.3]])
    def test_membership_and_normalization(self):
        x=np.random.default_rng(1).uniform(-1,1,(50,5))
        for m in memberships(x):self.assertTrue(np.all((m>=0)&(m<=1)))
        np.testing.assert_allclose(activation(x).sum(axis=1),1)
        np.testing.assert_allclose(activation(np.full((1,5),1e5)).sum(),1)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):activation([[np.nan]*5])
    def test_output_limits(self):
        u=control(np.ones((30,5)),np.full((N_RULES,2),100.))
        self.assertTrue(np.isfinite(u).all());self.assertTrue((u[:,0]<=VMAX).all());self.assertTrue((abs(u[:,1])<=WMAX).all())
    def test_swept_collision(self):
        c=segment_clearance(np.array([[1.,1.]]),np.array([[9.,1.]]),np.array([[[5.,1.,.2]]]))
        self.assertLess(c[0],0)
    def test_forward_motion_and_success(self):
        w=np.tile([1.,0.],(N_RULES,1));out=rollout(w,[self.map],True)
        self.assertEqual(out['status'][0],'success')
        np.testing.assert_allclose(out['path'][1,0],[1+VMAX*DT,1])
        self.assertAlmostEqual(out['time'][0],out['ticks'][0]*DT)
    def test_timeout(self):
        out=rollout(np.zeros((N_RULES,2)),[self.map]);self.assertEqual(out['status'][0],'timeout');self.assertEqual(out['ticks'][0],STEPS)
    def test_collision(self):
        m=dict(self.map,obstacles=[[2.,1.,.3]])
        out=rollout(np.tile([1.,0.],(N_RULES,1)),[m]);self.assertEqual(out['status'][0],'collision')
    def test_ga_repeatability_and_bounds(self):
        a,h,_=train([self.map],3,100,6,2);b,j,_=train([self.map],3,100,6,2)
        np.testing.assert_array_equal(a,b);self.assertEqual(h,j)
        self.assertEqual(a.shape,(N_RULES,2));self.assertTrue((abs(a)<=1).all())
    def test_map_reproducibility(self):
        a=make_map(1);b=make_map(1);self.assertEqual(a,b);self.assertTrue(reachable(a))
    def test_train_test_isolation(self):
        self.assertFalse(set(range(100,108)) & set(range(2000,2030)))
    def test_paired_conditions(self):
        w=prior();m=[self.map]*2
        r=rollout(np.array([w,w]),m)
        self.assertEqual(r['status'][0],r['status'][1]);self.assertEqual(r['length'][0],r['length'][1])
    def test_mixed_obstacle_counts(self):
        m=dict(self.map,obstacles=self.map['obstacles']+[[7.,8.,.3]])
        r=rollout(prior(),[self.map,m])
        self.assertEqual(len(r['status']),2)

if __name__=='__main__': unittest.main()
