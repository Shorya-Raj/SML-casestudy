# Input provenance and attribution

The two CSVs in `raw/` are unchanged prepared split files acquired from the official UNSW shared folder (`CSV Files/Training and Testing Sets`). Acquisition details and SHA-256 digests are recorded in `ACTION_LOG.md`, the audit JSON, and model JSON. The scripts check the staged digests before modelling. The full raw packet-capture archive is outside this project.

Git attributes preserve the raw CSVs and dated archives byte for byte. This prevents Windows line-ending conversion from invalidating acquisition hashes or archive manifests.

[Official dataset page and academic-use terms](https://research.unsw.edu.au/projects/unsw-nb15-dataset). Academic use is permitted under the authors' stated terms. Commercial use requires agreement with the authors. Cite the dataset authors' requested works as well as the five recent journal papers used for the course literature review.

## Dataset works listed by the creators

1. Moustafa, N., and Slay, J. (2015). *UNSW-NB15: a comprehensive data set for network intrusion detection systems*. MilCIS, IEEE.
2. Moustafa, N., and Slay, J. (2016). *The evaluation of Network Anomaly Detection Systems: Statistical analysis of the UNSW-NB15 dataset and the comparison with the KDD99 dataset*. Information Security Journal: A Global Perspective.
3. Moustafa, N., et al. (2017). *Novel geometric area analysis technique for anomaly detection using trapezoidal area estimation on large-scale networks*. IEEE Transactions on Big Data.
4. Moustafa, N., et al. (2017). *Big data analytics for intrusion detection system: statistical decision-making using finite Dirichlet mixture models*. Data Analytics and Decision Support for Cybersecurity, Springer, 127–156.
5. Sarhan, M., Layeghy, S., Moustafa, N., and Portmann, M. *NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems*. BDTA 2020 / WiCON 2020 proceedings, Springer.

Follow the links on the official page for complete publisher records and the final citation style. This list records dataset attribution and is separate from the course's recent-paper requirement. The CSVs retain the creators' terms; no repository-wide software license is applied to them.
