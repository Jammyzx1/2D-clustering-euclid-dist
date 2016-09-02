# 2D-clustering-euclid-dist
A basic python script to generate an even number of clusters based on 2D coordinates and Euclidean distance.

As input the script expects a csv file of three columns and an undetermined number of rows. Column 1 should be a label, column 2 the first coordinate and column 3 the second coordinate.

This script is currently limited to producing an even number of clusters.  

The algorithm is as follows:

    For all coordinates do :
    |  Calculate the separating distances
    |  Store distances such that column and row indicies map to the raw data array row indicies
    end 

    While there are lss than the ask for number of nodes :
    |  For all separating distances :
    |  |  find the maximum separating distances and the points which are involved
    |  |  If the points have not been used before :
    |  |  |  store the points as nodes to cluster around
    |  |  end   
    |  end
    end

    For all coordinates find the node point which is closest:
    |  add the coordinates of the point to the list of closet points related to the node
    end  

A single file is output "Grouped.csv", which lists to groups. This will be overwritten by running it all again.
