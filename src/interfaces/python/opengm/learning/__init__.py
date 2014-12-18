from _learning import *
import numpy
import struct
from opengm import index_type,value_type, label_type

DatasetWithHammingLoss.lossType = 'hamming'
DatasetWithGeneralizedHammingLoss.lossType = 'generalized-hamming'




def _extendedLearn(self, infCls, parameter = None):
    if parameter is None:
        import opengm
        parameter = opengm.InfParam()
    cppParam  =  infCls.get_cpp_parameter(operator='adder',accumulator='minimizer',parameter=parameter)
    self._learn(cppParam)

GridSearch_HammingLoss.learn  =_extendedLearn
GridSearch_GeneralizedHammingLoss.learn  =_extendedLearn
StructMaxMargin_Bundle_HammingLoss.learn = _extendedLearn
StructMaxMargin_Bundle_GeneralizedHammingLoss = _extendedLearn
        
def createDataset(loss='hamming', numInstances=0):
    
    if loss not in ['hamming','h','gh','generalized-hamming']:
        raise RuntimeError("loss must be 'hamming' /'h' or 'generalized-hamming'/'gh' ")    

    if loss in ['hamming','h']:
        return DatasetWithHammingLoss(int(numInstances))
    elif loss in ['generalized-hamming','gh']:
        return DatasetWithGeneralizedHammingLoss(int(numInstances))
    else:
        raise RuntimeError("loss must be 'hamming' /'h' or 'generalized-hamming'/'gh' ")   




def gridSearchLearner(dataset, lowerBounds, upperBounds, nTestPoints):

    if dataset.__class__.lossType == 'hamming':
        learnerCls = GridSearch_HammingLoss
        learnerParamCls = GridSearch_HammingLossParameter
    elif dataset.__class__.lossType == 'generalized-hamming':
        learnerCls = GridSearch_GeneralizedHammingLoss
        learnerParamCls = GridSearch_GeneralizedHammingLossParameter

    nr = numpy.require 
    sizeT_type = 'uint64'

    if struct.calcsize("P") * 8 == 32:
        sizeT_type = 'uint32'

    param = learnerParamCls(nr(lowerBounds,dtype='float64'), nr(lowerBounds,dtype='float64'), 
                           nr(lowerBounds,dtype=sizeT_type))

    learner = learnerCls(dataset, param)
    return learner



def structMaxMarginLearner(dataset, regularizerWeight=1.0, minGap=1e-5, nSteps=0, optimizer='bundle'):
    if optimizer != 'bundle':
        raise RuntimeError("Optimizer type must be 'bundle' for now!")

    if dataset.__class__.lossType == 'hamming':
        learnerCls = StructMaxMargin_Bundle_HammingLoss
        learnerParamCls = StructMaxMargin_Bundle_HammingLossParameter
    elif dataset.__class__.lossType == 'generalized-hamming':
        learnerCls = StructMaxMargin_Bundle_GeneralizedHammingLoss
        learnerParamCls = StructMaxMargin_Bundle_GeneralizedHammingLossParameter

    param = learnerParamCls(regularizerWeight, minGap, nSteps)
    learner = learnerCls(dataset, param)
    
    return learner


def lPottsFunctions(nFunctions, numberOfLabels, features, weightIds):

    # check that features has the correct shape
    if features.ndim != 2:
        raise RuntimeError("feature must be two-dimensional")
    if features.shape[0] != nFunctions :
        raise RuntimeError("nFunctions.shape[0] must be equal to nFunctions")


    # check that weights has the correct shape
    if features.ndim != 1:
        raise RuntimeError("weightIds must be one-dimensional")
    if weightIds.shape[0] != features.shape[1] :
        raise RuntimeError("weightIds.shape[0]  must be equal to features.shape[1]")


    # require the correct types
    features = numpy.require(features, dtype=value_type)
    weightIds = numpy.require(weightIds, dtype=index_type)
    numberOfLabels = int(numberOfLabels)
    nFunctions = int(nFunctions)

    # do the c++ call here
    # which generates a function generator

    raise RuntimeError("not yet implemented")

def lUnaryFunctions(nFunctions, numberOfLabels, features, weightIds):
    raise RuntimeError("not yet implemented")




