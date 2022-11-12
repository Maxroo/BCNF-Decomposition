# Counts the number of steps required to decompose a relation into BCNF.

from relation import *
from functional_dependency import *

#Hao-Tse Wu V00951088

# You should implement the static function declared
# in the ImplementMe class and submit this (and only this!) file.
# You are welcome to add supporting classes and methods in this file.

bcnf_list= []   #store bcnf decom in choosen order per call of bcnf_decom has to be global value
all_bcnf_list = [] #store all bcnf decom version has to be global value
class ImplementMe:
    # Returns the number of recursive steps required for BCNF decomposition
    #
    # The input is a set of relations and a set of functional dependencies.
    # The relations have *already* been decomposed.
    # This function determines how many recursive steps were required for that
    # decomposition or -1 if the relations are not a correct decomposition.


    
    @staticmethod
    def DecompositionSteps( relations, fds ):
        all_relation = [] #store all relation in list 
        fd_dict = [] #store fd info in a list
        all_left = [] #store all left value in the fds
        all_closure = [] #store all closures/ same index as all left
        
        #check the decom# given by the call
        decomposition_num = len(relations.relations) - 1
        
        #store prev decom relation 
        original_relation = set()
        
        for items in relations.relations:
            all_relation.append(items)
            for item in items.attributes:
                original_relation.add(item)
        is_all_superkey = True
        #store all missing relation
        missing_relation = set.copy(original_relation)
        for item in fds.functional_dependencies:
            if item.left_hand_side not in all_left:
                all_left.append(item.left_hand_side)

            fd_dict.append( item.left_hand_side)

            fd_dict.append( item.right_hand_side)
            

        for i in range(len(all_left)):
            all_closure.append(ImplementMe.find_closure(fds, all_left[i].copy()))
            
        d_relations = []
        d_relations.append(original_relation)
            
        n_relations = Relation(original_relation)
            
        #create variant of fd_dict and call bcnf decom to find different version of bcnf decomposition
        count = len(fd_dict)
        loop = count/2
        alist = [1,2,3,4,5]
        ImplementMe.bcnf_decom(n_relations,fd_dict)
        return bcnf_list

    #recursivly call self and add final bcnf relation to bcnf_list
    def bcnf_decom(n_relations, fd_dict):
        all_left = []
        all_closure = []
        all_right = []
        all_fd = set()
        d_relations = n_relations.attributes
        
        for i in range(len(fd_dict)):
            if i%2 == 0 :
                all_left.append(fd_dict[i])
                all_right.append(fd_dict[i+1])
                all_fd.add(FunctionalDependency(fd_dict[i], fd_dict[i+1]))
        new_fds = FDSet(all_fd)
            
        all_closure2 = []
        for i in range(len(all_left)):
            all_closure.append(ImplementMe.find_closure(new_fds, all_left[i].copy()))
            
        for count in range(len(all_left)):
            if(not d_relations.issubset(all_closure[count]) and all_left[count].issubset(d_relations)):
                r1 = set()
                r2 = set()
                
                closure_set = all_closure[count]
                r1 = r1.union(closure_set)
                r2 = d_relations - r1
                r2 = r2.union(all_left[count])

                all_left_copy = all_left.copy()
                all_closure_copy = all_closure.copy()
                
                fd_project_r1 = ImplementMe.project_fd(r1, fd_dict)
                fd_project_r2 = ImplementMe.project_fd(r2, fd_dict)
                
                new_fd_dict_r1 = []
                for item in fd_project_r1:
                    new_fd_dict_r1.append(item.left_hand_side)
                    new_fd_dict_r1.append(item.right_hand_side)

                new_fd_dict_r2 = []
                for item in fd_project_r2:
                    new_fd_dict_r2.append(item.left_hand_side)
                    new_fd_dict_r2.append(item.right_hand_side)
                
                relaiton_r1 = Relation(r1)
                relaiton_r2 = Relation(r2)
                ImplementMe.bcnf_decom(relaiton_r1, new_fd_dict_r1)
                return ImplementMe.bcnf_decom(relaiton_r2, new_fd_dict_r2)
        bcnf_list.append(n_relations)
        return n_relations
    
    #return projected_fd per call
    def project_fd(out_relation, fd_dict):
        project_fdset = []
        for i in range(len(fd_dict)):
            if i%2 == 0:
                if fd_dict[i].issubset(out_relation) and fd_dict[i+1].issubset(out_relation):
                    project_fdset.append(FunctionalDependency(fd_dict[i], fd_dict[i+1]))
        return project_fdset

    #return closure per call
    def find_closure(fds, lhs):
        closure = lhs
        is_there_more = True
        while is_there_more:
            is_there_more = False
            for item in fds.functional_dependencies:
                if item.left_hand_side.issubset(closure) and not item.right_hand_side.issubset(closure):
                    is_there_more = True
                    closure.update(item.right_hand_side)
        return closure
    
    def check_is_all_superkey(all_closure, relation):
        is_all_superkey = True
        for closure in all_closure:
            if closure < relation:
                is_all_superkey = False    
        return is_all_superkey


    def test_is_bncf():
        relations = RelationSet({Relation({'a','c','b'})})
        fds = FDSet({FunctionalDependency({'a','b'}, {'c'}), \
                FunctionalDependency({'c'}, {'b'}) })

        print(ImplementMe.DecompositionSteps( relations, fds )) 
        
ImplementMe.test_is_bncf()