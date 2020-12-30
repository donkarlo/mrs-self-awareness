from mmath.linearalgebra.BiOpr import BiOpr
from state import ObservationCompositTimeSerie
from state.State import State
from state.filter import Filter
from mmath.linearalgebra import Matrix
import Innovation
class Kalman(Filter):
    '''
    process model: x_k=Fx_{k-1}+Bu_{k-1}+w_k, F:State transition matrix, B: Control-Input matrix
    Process noise vector: w_k ~ N(0.Q), Q: Process noise covariance matrix
    -----Paired with-----
    measurement model: z_k=Hx_{k-1}=v_{k}
    measurment/observation noise vector: v_k ~ N(0,R), R: measurement noise cov matrix
    -----Notation---------
    From here: -: predicted/prior estimation
    -----Prediction-------
    Predicted state estimate x^{~-}_{k}=Fx^{~+}_{k-1}+Bu_{k-1}, -:prior dist +:postrior dist
    P^{-}_{k}=FP^{+}_{k-1}F^{T}+Q, P:state error covariance
    -----update-----------
    Mesurement residual: y^{~}_{k} = z_k-Hx^{^-}_{k}
    Kalman gain: K_{k} = P^{-}_{k}H^{T}(R+HP^{-}_{k}H^{T})^{-1}
    Updated state estimate: x^{^+}_{k}=x^{^-}_{k}+K_ky^{~}
    Updated error estimate: P^{+}_{k} = (I-K_{k}H)P^{-}_{k}
    ----------initial guesses ---------------
    x0Post: initial guess of state filter, initial guess of state
    p0Post: initial, posterior state error covariance, initial guess of error cov
    1. To keep up with intial ignorance rule please send larg values
    2. The more x0Post is unceratin the larger poPost should be
    '''
    def __init__(self, observationSeri:ObservationCompositTimeSerie, x0Post:State, p0Post:Matrix, f:Matrix, b:Matrix, q:Matrix, h:Matrix, r:Matrix):
        self._r = r
        self._h = h
        self._q = q
        self._f = f
        self._b = b
        self._p0Post = p0Post
        self._observationSeri = observationSeri
        self._x0Post = x0Post

    def __update(self):
        pass

    def __predict(self):
        pass

    def __getInnovation(self)->Matrix:
        ino = Innovation(self.getLastObservation(),self._h,self.getPriorPrediction())
        return ino.getInnovation()

    def getPriorPrediction(self)->Matrix:
        pass


    def getLastObservation(self)->Matrix:
        return self._observationSeri[len(self._observationSeri)]
