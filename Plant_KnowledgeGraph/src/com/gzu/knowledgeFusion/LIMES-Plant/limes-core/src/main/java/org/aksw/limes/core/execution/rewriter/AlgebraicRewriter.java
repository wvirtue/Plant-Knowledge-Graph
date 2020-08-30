package org.aksw.limes.core.execution.rewriter;

import java.util.ArrayList;
import java.util.List;

import org.aksw.limes.core.datastrutures.LogicOperator;
import org.aksw.limes.core.io.ls.LinkSpecification;
import org.aksw.limes.core.io.parser.Parser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Implements the algebraic rewriter class. The idea is that the rewriter gets
 * as input a link specification returns an equivalent yet probably more
 * time-efficient link specification.
 *
 *
 * @author Axel-C. Ngonga Ngomo (ngonga@informatik.uni-leipzig.de)
 * 
 * @version 1.0
 */
public class AlgebraicRewriter extends Rewriter {
    static Logger logger = LoggerFactory.getLogger(AlgebraicRewriter.class);

    /**
     * Rewrites a Link Specification. The idea is that the rewriter gets as
     * input a link specification returns an equivalent yet probably more
     * time-efficient link specification.
     *
     * @param spec,
     *            Input link specification
     * @return the input link specification.
     */
    @Override
    public LinkSpecification rewrite(LinkSpecification spec) {
        if (spec.isEmpty())
            throw new IllegalArgumentException();
        // rewrite only non-atomic specs
        if (spec.size() <= 1)
            return spec;
        int oldSize;
        int newSize = spec.size();
        LinkSpecification result = spec;
        try {
            do {
                System.out.println(spec);
                oldSize = newSize;
                spec = updateThresholds(spec);
                spec = computeAllDependencies(spec);
                spec = collapseSpec(spec);
                spec = removeUnaryOperators(spec);
                spec = removeDuplicates(spec);
                newSize = spec.size();
                result = spec;
            } while (newSize < oldSize);
        } catch (Exception e) {
            logger.error(e.getMessage());
            e.printStackTrace();
        }
        return result;
    }

    /**
     * Updates the thresholds within the input link specification.
     *
     * @param spec,
     *            The input link specification
     * @return Return spec with updated weights
     */
    public LinkSpecification updateThresholds(LinkSpecification spec) {
        // should not happen
        if (spec == null)
            return spec;
        if (spec.isEmpty())
            return spec;
        if (spec.isAtomic())
            return spec;
        // does not work for atomic specs
        if (!spec.isAtomic()) {
            // only works for null filters
            if (spec.getFilterExpression() == null) {
                double min = 1f;
                // get minimum over all children
                for (LinkSpecification child : spec.getChildren()) {
                    if (child.getThreshold() < min) {
                        min = child.getThreshold();
                    }
                }
                // if spec threshold smaller than miminum then set to 0
                if (spec.getThreshold() <= min) {
                    spec.setThreshold(0);
                }
            }
            // if spec has children then run update for children as well
            for (LinkSpecification child : spec.getChildren()) {
                child = updateThresholds(child);
            }
        }
        return spec;
    }

    /**
     * Removes duplicated specifications from specification.
     *
     * @param spec,
     *            The input link specification
     * @return spec, de-duplicated specification
     */
    public LinkSpecification removeDuplicates(LinkSpecification spec) {

        if (!spec.isAtomic()) {
            if (spec.getChildren().size() == 2) {
                LinkSpecification left = removeDuplicates(spec.getChildren().get(0));
                LinkSpecification right = removeDuplicates(spec.getChildren().get(1));
                if (left.equals(right)) {
                    spec = left;
                    double theta = Math.max(spec.getThreshold(), left.getThreshold());
                    spec.setThreshold(theta);
                }
            }
        }

        return spec;
    }

    /**
     * Removes unary operators from a specification.
     *
     * @param spec,
     *            The input link specification
     * @return Cleaned up spec
     */
    public LinkSpecification removeUnaryOperators(LinkSpecification spec) {
        System.out.println("removeUnaryOperators: " + spec);
        System.out.println("removeUnaryOperators: " + spec.isAtomic());

        if (!spec.isAtomic()) {
            // if the LS has more than one child, it propagates the removal to
            // the children
            if (spec.getFilterExpression() == null && spec.getChildren().size() == 1) {
                // don't forget to update the threshold while lifting the branch
                double theta = Math.max(spec.getThreshold(), spec.getChildren().get(0).getThreshold());
                System.out.print("Old spec = " + spec);
                spec = spec.getChildren().get(0);
                spec.setThreshold(theta);
                System.out.println("New spec = " + spec);
                System.out.println(spec.isAtomic());
            }
            if (!spec.isAtomic()) {
                List<LinkSpecification> newChildren = new ArrayList<LinkSpecification>();
                for (LinkSpecification child : spec.getChildren()) {
                    System.out.println("child spec = " + child);
                    newChildren.add(removeUnaryOperators(child));
                }
                spec.setChildren(newChildren);
            }
        }
        return spec;
    }

    /**
     * Checks whether source depends on target, i.e., whether the mapping
     * generated by source is a subset of the mapping generated by target.
     * Returns 0 if no dependency is found, 1 if target is included in source,
     * -1 if source is included in target and +2 if they are equivalent.
     *
     * @param source
     *            Source link spec
     * @param target
     *            Target link spec
     * @return -1, 0, +1 or +2
     */
    public LinkSpecification computeAtomicDependency(LinkSpecification source, LinkSpecification target) {
        // only works for atomic properties
        if (!source.isAtomic() || !target.isAtomic()) {
            return source;
        }
        // compute the source and target properties used. Only works if the
        // properties
        // used by the spec are the same
        if (getProperties(source).equals(getProperties(target))) {
            String measure1 = getMeasure(source);
            String measure2 = getMeasure(target);
            if (measure1.equals(measure2)) {
                // !!!!!!!!!!!!!!!!!!!!!!!!!!!! < not <=
                if (source.getThreshold() <= target.getThreshold()) {
                    source.addDependency(target);
                } else {
                    // !!!!!!!!!!!!!!!!!!!!!!!! WHAT?????
                    double t1 = source.getThreshold();
                    double t2 = target.getThreshold();
                    if (measure1.equals("trigrams")) {
                        // works for jaro vs. jaro-winkler
                        //
                    } else if (measure2.equals("overlap")) {// WHAT?????
                        if (measure2.equals("jaccard") && t2 <= 2 * t1 / (1 + t1)) {
                            source.addDependency(target);
                        }
                    }
                }
            }
        }
        return source; // nothing found
    }

    /**
     * Returns the properties that are used for the comparison. Only works for
     * atomic specifications.
     *
     * @param spec,
     *            The input specification
     * @return List of properties used in the specification
     */
    public List<String> getProperties(LinkSpecification spec) {
        List<String> result = new ArrayList<String>();
        if (spec.isAtomic()) {
            Parser p = new Parser(spec.getFilterExpression(), spec.getThreshold());
            result.add(p.getLeftTerm());
            result.add(p.getRightTerm());
        }
        return result;
    }

    /**
     * Returns the measure used in the specification.
     *
     * @param spec,
     *            The input specification
     * @return Measure used in the specification, null if the specification is
     *         not atomic
     */
    public String getMeasure(LinkSpecification spec) {
        if (spec.isAtomic()) {
            return spec.getFilterExpression().substring(0, spec.getFilterExpression().indexOf("("));
        } else {
            return null;
        }
    }

    /**
     * Updates all dependencies within a specification.
     *
     * @param spec,
     *            The input specification
     * @return spec, with all dependencies updated
     */
    public LinkSpecification computeAllDependencies(LinkSpecification spec) {
        spec = computeAtomicDependencies(spec);
        spec = computeNonAtomicDependencies(spec);
        for (LinkSpecification ls : spec.getAllLeaves()) {
            System.out.println(ls);
            System.out.println(ls.getDependencies());
        }
        return spec;
    }

    /**
     * Updates the non-atomic dependencies of a link specification.
     *
     * @param spec,
     *            The input specification
     * @return spec, updated specification with non-atomic dependencies
     */
    public LinkSpecification computeNonAtomicDependencies(LinkSpecification spec) {
        if (!spec.isAtomic()) {
            List<LinkSpecification> newDependencies = null;
            List<LinkSpecification> newChildren = new ArrayList<LinkSpecification>();
            // first update dependencies of children
            for (LinkSpecification child : spec.getChildren()) {
                newChildren.add(computeNonAtomicDependencies(child));
            }
            spec.setChildren(newChildren);
            // then update spec itself
            // if operator = AND, then dependency is intersection of all
            // dependencies
            // if all children of a conjuction depend on L' then the father of
            // the conjuction depends on L'
            if (spec.getOperator() == LogicOperator.AND && spec.getChildren().get(0).hasDependencies()) {
                newDependencies = spec.getChildren().get(0).getDependencies();
                for (int i = 1; i < spec.getChildren().size(); i++) {
                    if (!spec.getChildren().get(i).hasDependencies()) {
                        break;
                    } else {
                        newDependencies.retainAll(spec.getChildren().get(i).getDependencies());
                    }
                }
            }
            // if operator = OR, then merge all
            if (spec.getOperator() == LogicOperator.OR) {
                newDependencies = new ArrayList<LinkSpecification>();
                for (LinkSpecification child : spec.getChildren()) {
                    if (child.hasDependencies()) {
                        newDependencies.addAll(child.getDependencies());
                    }
                }
            }
            // System.out.println(spec);
            // System.out.println("Dependencies: " + newDependencies);
            spec.setDependencies(null);

            if (newDependencies != null) {
                for (LinkSpecification d : newDependencies) {
                    if (d.getThreshold() > spec.getThreshold() || spec.getThreshold() == 0) {
                        spec.addDependency(d);
                    }
                }
            }
        }
        return spec;
    }

    /**
     * Computes all atomic dependencies within a link specification.
     *
     * @param spec,
     *            The input specification
     * @return spec, updated specification with atomic dependencies
     */
    public LinkSpecification computeAtomicDependencies(LinkSpecification spec) {
        List<LinkSpecification> leaves = spec.getAllLeaves();
        // compute the dependency between leaves
        for (int i = 0; i < leaves.size(); i++) {
            // reset dependencies
            leaves.get(i).setDependencies(new ArrayList<LinkSpecification>());
            for (int j = 0; j < leaves.size(); j++) {
                if (i != j) {
                    leaves.set(i, computeAtomicDependency(leaves.get(i), leaves.get(j)));
                }
            }
        }
        return spec;
    }

    /**
     * Collapses a spec by making use of the dependencies within the
     * specification.
     *
     * @param spec,
     *            The input specification
     * @return Collapsed spec, i.e., specification where dependencies have been
     *         removed
     */
    public LinkSpecification collapseSpec(LinkSpecification spec) {
        if (spec == null)
            return spec;
        if (spec.isAtomic()) { // || spec.isEmpty()) {
            return spec;
        }
        // first collapse children which depend on each other
        if (spec.getOperator() == LogicOperator.AND) {
            List<LinkSpecification> newChildren = new ArrayList<LinkSpecification>();
            newChildren.addAll(spec.getChildren());
            // child is a superset of its dependencies, thus
            // if one of its dependency is a child of the current node, then
            // no need to compute child
            for (LinkSpecification child : spec.getChildren()) {
                if (child.hasDependencies()) {
                    System.out.println("Dependency found");
                    for (LinkSpecification dependency : child.getDependencies()) {
                        System.out.println("Dependency : " + dependency);
                        if (newChildren.contains(dependency)) {
                            // ensures that at least one child is kept, in case
                            // of cyclic dependencies
                            // quick fix. Might not work
                            if (newChildren.size() > 1) {
                                newChildren.remove(child);
                                System.out.println("Children after removal: " + newChildren);
                            }
                        }
                    }

                }

            }
            spec.setChildren(newChildren);
        } else if (spec.getOperator() == LogicOperator.OR) {
            List<LinkSpecification> newChildren = new ArrayList<LinkSpecification>();
            newChildren.addAll(spec.getChildren());

            for (LinkSpecification child : spec.getChildren()) {
                if (child.hasDependencies()) {
                    for (LinkSpecification dependency : child.getDependencies()) {
                        // all entries of dependency contained in child, so
                        // no need to compute it
                        if (newChildren.contains(dependency)) {
                            // ensures that at least one child is kept, in case
                            // of cyclic dependencies
                            // quick fix. Might not work
                            if (newChildren.size() > 1) {
                                newChildren.remove(dependency);
                            }
                        }
                    }
                }
            }
            spec.setChildren(newChildren);
        }
        List<LinkSpecification> newChildren = new ArrayList<LinkSpecification>();
        // now collapse remaining children
        for (LinkSpecification child : spec.getChildren()) {
            newChildren.add(collapseSpec(child));
        }
        spec.setChildren(newChildren);
        return spec;
    }

}
