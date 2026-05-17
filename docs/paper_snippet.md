# Manuscript-ready snippet

The following text can be adapted into a paper's Method, Principles, or Reproducibility subsection.

## Membership-function definition

Let \(U\subseteq \mathbb{R}\) denote the universe of discourse and let \(\mu_A:U\rightarrow[0,1]\) denote the membership function for fuzzy set \(A\).  In this study, we used a sigmoid-composed S membership function to allow membership differences to be clearly discriminated near a focal value while becoming less sensitive in distant regions of the universe scale.  The logistic transformation is

\[
f(u;\alpha,u_*)=\frac{1}{1+\exp[-\alpha(u-u_*)]},
\]

where \(u_*\) is the focal value.  Given a far value \(u_q\) and a quantile \(q\in(0.5,1)\), the gain was set as

\[
\alpha=\frac{\log\{q/(1-q)\}}{u_q-u_*},
\]

so that \(f(u_*)=0.5\) and \(f(u_q)=q\).  With \(p=1-q\), the membership function was defined as

\[
\mu_A(u)=S(f(u;\alpha,u_*);p,q),
\]

where

\[
S(x;p,q)=
\begin{cases}
0, & x\le p,\\
2\left(\dfrac{x-p}{q-p}\right)^2, & p<x\le \dfrac{p+q}{2},\\
1-2\left(\dfrac{x-q}{q-p}\right)^2, & \dfrac{p+q}{2}<x\le q,\\
1, & q<x.
\end{cases}
\]

The implementation used `fuzzy-membership-kit` version `0.2.0.dev0`.  The exact membership configuration, package commit, and derived score files are provided in the accompanying repository.

## Example parameter statement

For the VAS universe \([0,100]\), the increasing fuzzy set `high` used \(u_*=50\), \(u_q=90\), and \(q=0.9\).  Thus,

\[
\alpha=\frac{\log(0.9/0.1)}{90-50}=0.05493\ldots.
\]

Membership is 0.5 at \(u=50\), reaches 1.0 at \(u=90\), and changes more gradually for values farther from the focal region.
