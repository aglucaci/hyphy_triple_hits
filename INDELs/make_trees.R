# Generate a newick tree.
# Author: Alexander G. Lucaci

#http://www.phytools.org/eqg/Exercise_3.2/
#https://cran.r-project.org/web/packages/ape/ape.pdf

# IMPORTS
library(ape)

# Declares
#set.seed(24)
#https://www.rdocumentation.org/packages/compositions/versions/1.40-3/topics/rnorm
mat <- matrix(abs(rnorm(30, 2, 1.5))) # make branch length a distribution, <1 to about 8

## simulate a phylogeny

# branch lengths drawn from a distribution, see above.
#tree <- rtree(n = 30, rooted = TRUE, br = mat)

# uniform distribution of branch lengthsi
#tree <- rtree(n = 30, rooted = TRUE, br = TRUE)

#generic way to make tree
tree <- rtree(n = 30, rooted = TRUE) #make the n a distribution like 10-50

#plot the tree
plot(tree, edge.width = 2)

#write to file
write.tree(tree, file = "example.trees")

head(tree)


## END OF FILE