#!/usr/bin/env python

from ROOT import TMVA, TFile, TTree, TCut
from subprocess import call
from os.path import isfile

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.regularizers import l2
from keras.optimizers import SGD

# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

output = TFile.Open('TMVA.root', 'RECREATE')
factory = TMVA.Factory('TMVAClassification', output,
                       '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Classification')

# Load data

dataS = TFile.Open('~/Test/Testy/out_sig.root')
dataB = TFile.Open('~/Test/Testy/out_bkg.root')
signal = dataS.Get('ntuple')
background = dataB.Get('ntuple')

dataloader = TMVA.DataLoader('dataset')
#for branch in signal.GetListOfBranches():
 #   dataloader.AddVariable(branch.GetName())

dataloader.AddVariable( "xp")
dataloader.AddVariable( "yp")
dataloader.AddVariable( "zp")
dataloader.AddVariable( "pxp")
dataloader.AddVariable( "pyp")
dataloader.AddVariable( "pzp")
dataloader.AddVariable( "xm")
dataloader.AddVariable( "ym")
dataloader.AddVariable( "zm" )
dataloader.AddVariable( "pxm")
dataloader.AddVariable( "pym")
dataloader.AddVariable( "pzm")
'''dataloader.AddVariable( "dist")
dataloader.AddVariable( "DeltPhi")'''
dataloader.AddVariable( "mu_likep")
dataloader.AddVariable( "mu_likem")
dataloader.AddSpectator( "minv" )


dataloader.AddSignalTree(signal, 1.0)
dataloader.AddBackgroundTree(background, 1.0)
dataloader.PrepareTrainingAndTestTree(TCut(''),
                                      'SplitMode=Random:NormMode=NumEvents:!V')

# Define initialization
#def normal(shape, name=None):
#	return initializations.normal(shape, scale=0.05, name=name)


# Generate model

# Define model
model = Sequential()
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
model.add(Dense(64,  activation='relu', W_regularizer=l2(1e-5), input_dim=14))
#model.add(Dense(32, init=normal, activation='relu', W_regularizer=l2(1e-5)))
#model.add(Dense(2, init=normal, activation='softmax'))

model.add(Dense(32, activation='relu', W_regularizer=l2(1e-5)))
model.add(Dense(8, activation='softmax'))
model.add(Dense(2,  activation='sigmoid'))

# Set loss and optimizer
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy',])
#model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy',])
# Compile model
#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Store model to file
model.save('model.h5')
model.summary()

# Book methods
#factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
#                   '!H:!V:Fisher:VarTransform=D,G')
factory.BookMethod(dataloader, TMVA.Types.kPyKeras, 'PyKeras',
                   'H:!V:VarTransform=D,G:FilenameModel=model.h5:NumEpochs=100:BatchSize=32')
factory.BookMethod( dataloader,  TMVA.Types.kBDT, "BDT",
                           "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" )

# Run training, test and evaluation
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
