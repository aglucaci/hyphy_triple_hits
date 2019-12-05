#http://www.phytools.org/eqg/Exercise_3.2/

library(ape)

## simulate a phylogeny
tree <- rtree(n = 30)
plot(tree, edge.width = 2)


write.tree(tree, file = "example.trees")