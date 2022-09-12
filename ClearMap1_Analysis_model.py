# -*- coding: utf-8 -*-
"""
Example script to set up the parameters for the image processing pipeline
"""

#### = E-Dmz comments

#### Load "heatmaps generated previously" (density_counts.tif for each mouse)
#### Writes maps with mean and std
# -> controls-mean.raw and deprived-mean.raw, etc.)
#### pvals, psign (mean control v. deprived), pvalsc (color)
# -> controls_vs_deprived_pval_0.05.tif

#### then load files cells_ClearMap1_points_transformed.npy (??, one for each mouse)
#### and cells_ClearMap1_intensities
#### group 1 and group1i, pc and pci, pvals and pvalsi, psign and psigni, etc.
#### filtering pvalsi < 1 -> suffix "0" (ids0, pci0, pvals0, etc.)

#### create one table (counts), then the other (intensity)
#### sort by q-value is in fact sort by pvals







# import modules:

import ClearMap.Analysis.Statistics2hem as stat
#### readDataGroup
#### tTestVoxelization
#### colorPValues
#### countPointsGroupInRegions
#### tTestPointsInRegions
#### -> Statistics2hem, Label2hem don't exist in ClearMap2
#### however functions with same name exist in
# ClearMap.Analysis.Statistics.GroupStatistics
#### But there's no Label.py nor labelToName to be found
import ClearMap.Analysis.Label2hem as lbl
import ClearMap.IO.IO as io
import ClearMap.Alignment.Resampling as rsp
import numpy, os

#### Also FDR.estimateQValues, comes from ClearMap.Analysis.Tools.MultipleComparisonCorrection

# Base Directory, usually where your experiment is saved:
baseDirectory = '/media/data/Alba/Fos/200311-CM2-4animals'



# Voxel-based statistics:
########################

#Load the data (heat maps generated previously )


group1 = ['/media/data/Alba/Fos/200311-4/density_counts.tif',
          '/media/data/Alba/Fos/200311-7/density_counts.tif',
          '/media/data/Alba/Fos/200311-2/density_counts.tif',
          '/media/data/Alba/Fos/200311-9/density_counts.tif']
#          '/media/data/Alba/Fos/200311-1camk/density_counts.tif']
         # '/media/data/Alba/Fos/200311-4camk/density_counts.tif']

group2 = ['/media/data/Alba/Fos/200311-11/density_counts.tif',
          '/media/data/Alba/Fos/200311-2camk/density_counts.tif',
          '/media/data/Alba/Fos/200311-5camk/density_counts.tif',
          '/media/data/Alba/Fos/200311-11camk/density_counts.tif']



g1 = stat.readDataGroup(group1);
g2 = stat.readDataGroup(group2);



#Generated average and standard deviation maps
##############################################
g1a = numpy.mean(g1,axis = 0);
g1s = numpy.std(g1,axis = 0);

g2a = numpy.mean(g2,axis = 0);
g2s = numpy.std(g2,axis = 0);

io.writeData(os.path.join(baseDirectory, '200311-controls-mean.raw'), rsp.sagittalToCoronalData(g1a));
io.writeData(os.path.join(baseDirectory, '200311-controls-std.raw'), rsp.sagittalToCoronalData(g1s));

io.writeData(os.path.join(baseDirectory, '200311-deprived-mean.raw'), rsp.sagittalToCoronalData(g2a));
io.writeData(os.path.join(baseDirectory, '200311-deprived-std.raw'), rsp.sagittalToCoronalData(g2s));





#Generate the p-values map
#########################
#pcutoff: only display pixels below this level of significance

pvals, psign = stat.tTestVoxelization(g1.astype('float'), g2.astype('float'), signed = True, pcutoff = 0.05);

#color the p-values according to their sign (defined by the sign of the difference of the means between the 2 groups)
pvalsc = stat.colorPValues(pvals, psign, positive = [0,1], negative = [1,0]);
io.writeData(os.path.join(baseDirectory, '200311-controls_vs_deprived_pval_0.05.tif'), rsp.sagittalToCoronalData(pvalsc.astype('float32')));


#%%###########################################################################

# Regions-based statistics:
###########################

group1 = ['/media/data/Alba/Fos/200311-2/cells_ClearMap1_points_transformed.npy',
          '/media/data/Alba/Fos/200311-4/cells_ClearMap1_points_transformed.npy',
          '/media/data/Alba/Fos/200311-7/cells_ClearMap1_points_transformed.npy',
          '/media/data/Alba/Fos/200311-9/cells_ClearMap1_points_transformed.npy']
#          '/media/data/Alba/Fos/200311-1camk/cells_ClearMap1_points_transformed.npy']
#          '/media/data/Alba/Fos/200311-4camk/cells_ClearMap1_points_transformed.npy']

group2 = ['/media/data/Alba/Fos/200311-11/cells_ClearMap1_points_transformed.npy',
          '/media/data/Alba/Fos/200311-2camk/cells_ClearMap1_points_transformed.npy',
          '/media/data/Alba/Fos/200311-5camk/cells_ClearMap1_points_transformed.npy',
          '/media/data/Alba/Fos/200311-11camk/cells_ClearMap1_points_transformed.npy']

group1i = [fn.replace('cells_ClearMap1_points_transformed', 'cells_ClearMap1_intensities') for fn in group1];
group2i = [fn.replace('cells_ClearMap1_points_transformed', 'cells_ClearMap1_intensities') for fn in group2];



PathReg        = '/home/alba.vieitesprado/Programs/ClearMap_GUI/ClearMap/ClearMap_Ressources/Regions_annotations';
AnnotationFile = os.path.join(PathReg, 'Annotation_25_2-hemispheres-horizontal-ONLYFORANALYSIS.tif');

#ids, pc1, pc1i = stat.countPointsGroupInRegions(group1, intensityGroup = group1i, returnIds = True, labeledImage = AnnotationFile, returnCounts = True, collapse=True);
#pc2, pc2i = stat.countPointsGroupInRegions(group2, intensityGroup = group2i, returnIds = False, labeledImage = AnnotationFile, returnCounts = True, collapse=True);

ids, pc1, pc1i = stat.countPointsGroupInRegions(group1, intensityGroup = group1i, returnIds = True, labeledImage = AnnotationFile, returnCounts = True, collapse=None);
pc2, pc2i = stat.countPointsGroupInRegions(group2, intensityGroup = group2i, returnIds = False, labeledImage = AnnotationFile, returnCounts = True, collapse=None);


pvals, psign = stat.tTestPointsInRegions(pc1, pc2, pcutoff = None, signed = True);
pvalsi, psigni = stat.tTestPointsInRegions(pc1i, pc2i, pcutoff = None, signed = True, equal_var = True);

import ClearMap.Analysis.Tools.MultipleComparisonCorrection as FDR


iid = pvalsi < 1;

ids0 = ids[iid];
pc1i0 = pc1i[iid];
pc2i0 = pc2i[iid];
pc10 = pc1[iid];
pc20 = pc2[iid];
psigni0 = psigni[iid];
pvalsi0 = pvalsi[iid];
qvalsi0 = FDR.estimateQValues(pvalsi0);
psign0 = psign[iid];
pvals0 = pvals[iid];
qvals0 = FDR.estimateQValues(pvals0);


#make table

dtypes = [('id','int64'),('mean1','f8'),('std1','f8'),('mean2','f8'),('std2','f8'),('pvalue', 'f8'),('qvalue', 'f8'),('psign', 'int64')];
for i in range(len(group1)):
    dtypes.append(('count1_%d' % i, 'f8'));
for i in range(len(group2)):
    dtypes.append(('count2_%d' % i, 'f8'));
dtypes.append(('name', 'a256'));

table = numpy.zeros(ids0.shape, dtype = dtypes)
table["id"] = ids0;
table["mean1"] = pc1i0.mean(axis = 1)/1000000;
table["std1"] = pc1i0.std(axis = 1)/1000000;
table["mean2"] = pc2i0.mean(axis = 1)/1000000;
table["std2"] = pc2i0.std(axis = 1)/1000000;
table["pvalue"] = pvalsi0;
table["qvalue"] = qvalsi0;

table["psign"] = psigni0;
for i in range(len(group1)):
    table["count1_%d" % i] = pc10[:,i];
for i in range(len(group2)):
    table["count2_%d" % i] = pc20[:,i];
table["name"] = lbl.labelToName(ids0);


#sort by qvalue
ii = numpy.argsort(pvalsi0);
tableSorted = table.copy();
tableSorted = tableSorted[ii];

with open(os.path.join(baseDirectory, '200311-controls_vs_deprived-intensity_table-non-collapsed.csv'),'w') as f:
    f.write(', '.join([str(item) for item in table.dtype.names]));
    f.write('\n');
    for sublist in tableSorted:
        f.write(', '.join([str(item) for item in sublist]));
        f.write('\n');
    f.close();

#############################


#make table

dtypes = [('id','int64'),('mean1','f8'),('std1','f8'),('mean2','f8'),('std2','f8'),('pvalue', 'f8'),('qvalue', 'f8'),('psign', 'int64')];
for i in range(len(group1)):
    dtypes.append(('count1_%d' % i, 'f8'));
for i in range(len(group2)):
    dtypes.append(('count2_%d' % i, 'f8'));
dtypes.append(('name', 'a256'));

table = numpy.zeros(ids0.shape, dtype = dtypes)
table["id"] = ids0;
table["mean1"] = pc10.mean(axis = 1);
table["std1"] = pc10.std(axis = 1);
table["mean2"] = pc20.mean(axis = 1);
table["std2"] = pc20.std(axis = 1);
table["pvalue"] = pvals0;
table["qvalue"] = qvals0;

table["psign"] = psign0;
for i in range(len(group1)):
    table["count1_%d" % i] = pc10[:,i];
for i in range(len(group2)):
    table["count2_%d" % i] = pc20[:,i];
table["name"] = lbl.labelToName(ids0);


#sort by qvalue
ii = numpy.argsort(pvals0);
tableSorted = table.copy();
tableSorted = tableSorted[ii];

with open(os.path.join(baseDirectory, '200311-controls_vs_deprived-counts_table-non-collapsed.csv'),'w') as f:
    f.write(', '.join([str(item) for item in table.dtype.names]));
    f.write('\n');
    for sublist in tableSorted:
        f.write(', '.join([str(item) for item in sublist]));
        f.write('\n');
    f.close();


#############################################################################
