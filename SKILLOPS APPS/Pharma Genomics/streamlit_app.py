import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Pharma Genomics - scvi-tools",
    page_icon="🧬",
    layout="wide"
)

st.title("Pharma Genomics: Single-Cell Deep Learning Platform")
st.markdown("Deep learning-based single-cell analysis powered by **scvi-tools**")

MODEL_INFO = {
    "scVI": {
        "data_type": "scRNA-seq",
        "use_case": "Unsupervised integration, differential expression, imputation",
        "requires_labels": False,
        "description": "Variational autoencoder for scRNA-seq data. Performs batch correction, normalization, and dimensionality reduction in a unified probabilistic framework.",
    },
    "scANVI": {
        "data_type": "scRNA-seq + labels",
        "use_case": "Label transfer, semi-supervised integration",
        "requires_labels": True,
        "description": "Extension of scVI that leverages cell type annotations for semi-supervised learning and label transfer to unannotated cells.",
    },
    "totalVI": {
        "data_type": "CITE-seq (RNA + protein)",
        "use_case": "Multi-modal integration, protein denoising",
        "requires_labels": False,
        "description": "Joint model for RNA and protein data from CITE-seq experiments. Denoises protein measurements and integrates both modalities.",
    },
    "PeakVI": {
        "data_type": "scATAC-seq",
        "use_case": "Chromatin accessibility analysis",
        "requires_labels": False,
        "description": "Deep generative model for scATAC-seq data. Learns latent representations of chromatin accessibility profiles.",
    },
    "MultiVI": {
        "data_type": "Multiome (RNA + ATAC)",
        "use_case": "Joint modality analysis",
        "requires_labels": False,
        "description": "Integrates RNA and ATAC data from multiome experiments, handling missing modalities and batch effects.",
    },
    "DestVI": {
        "data_type": "Spatial + scRNA reference",
        "use_case": "Cell type deconvolution",
        "requires_labels": True,
        "description": "Deconvolves spatial transcriptomics spots into cell type proportions using a scRNA-seq reference.",
    },
    "veloVI": {
        "data_type": "RNA velocity",
        "use_case": "Transcriptional dynamics",
        "requires_labels": False,
        "description": "Variational inference approach to RNA velocity, providing uncertainty estimates for transcriptional dynamics.",
    },
    "sysVI": {
        "data_type": "Cross-technology",
        "use_case": "System-level batch correction",
        "requires_labels": False,
        "description": "Handles strong batch effects across different sequencing technologies and experimental systems.",
    },
}

tab1, tab2, tab3, tab4 = st.tabs(["Model Selection", "Pipeline Configuration", "Training Monitor", "Results"])

with tab1:
    st.header("Model Selection Guide")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("What data do you have?")
        data_type = st.radio(
            "Select your data type:",
            [
                "scRNA-seq (no labels)",
                "scRNA-seq (with cell type labels)",
                "CITE-seq (RNA + protein)",
                "scATAC-seq",
                "Multiome (RNA + ATAC)",
                "Spatial transcriptomics + scRNA reference",
                "RNA velocity data",
                "Cross-technology datasets",
            ],
        )

        data_type_to_model = {
            "scRNA-seq (no labels)": "scVI",
            "scRNA-seq (with cell type labels)": "scANVI",
            "CITE-seq (RNA + protein)": "totalVI",
            "scATAC-seq": "PeakVI",
            "Multiome (RNA + ATAC)": "MultiVI",
            "Spatial transcriptomics + scRNA reference": "DestVI",
            "RNA velocity data": "veloVI",
            "Cross-technology datasets": "sysVI",
        }

        recommended_model = data_type_to_model[data_type]

    with col2:
        st.subheader(f"Recommended: {recommended_model}")
        info = MODEL_INFO[recommended_model]
        st.info(info["description"])
        st.markdown(f"**Data Type:** {info['data_type']}")
        st.markdown(f"**Use Case:** {info['use_case']}")
        st.markdown(f"**Requires Labels:** {'Yes' if info['requires_labels'] else 'No'}")

    st.divider()
    st.subheader("All Available Models")
    model_df = pd.DataFrame(
        [
            {"Model": k, "Data Type": v["data_type"], "Use Case": v["use_case"]}
            for k, v in MODEL_INFO.items()
        ]
    )
    st.dataframe(model_df, use_container_width=True, hide_index=True)

with tab2:
    st.header("Pipeline Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Data Preparation")
        batch_key = st.text_input("Batch key column", value="batch")
        n_hvgs = st.slider("Number of highly variable genes", 1000, 5000, 2000, step=500)
        min_genes = st.number_input("Min genes per cell", value=200, min_value=50)
        min_cells = st.number_input("Min cells per gene", value=3, min_value=1)
        layer = st.selectbox("Count layer", ["counts", "raw_counts", "X"])

    with col2:
        st.subheader("Model Training")
        selected_model = st.selectbox("Model", list(MODEL_INFO.keys()))
        n_epochs = st.slider("Max epochs", 50, 500, 200, step=50)
        n_latent = st.slider("Latent dimensions", 5, 50, 30, step=5)
        learning_rate = st.select_slider(
            "Learning rate",
            options=[1e-4, 5e-4, 1e-3, 5e-3, 1e-2],
            value=1e-3,
            format_func=lambda x: f"{x:.0e}",
        )
        use_gpu = st.checkbox("Use GPU (if available)", value=True)
        early_stopping = st.checkbox("Early stopping", value=True)

    st.divider()
    st.subheader("Generated Pipeline Commands")

    commands = f"""# 1. Validate input data
python scripts/validate_adata.py input.h5ad --batch-key {batch_key} --suggest

# 2. Prepare data (QC, HVG selection)
python scripts/prepare_data.py input.h5ad prepared.h5ad \\
    --batch-key {batch_key} \\
    --n-hvgs {n_hvgs} \\
    --min-genes {min_genes} \\
    --min-cells {min_cells} \\
    --layer {layer}

# 3. Train model
python scripts/train_model.py prepared.h5ad results/ \\
    --model {selected_model.lower()} \\
    --batch-key {batch_key} \\
    --n-latent {n_latent} \\
    --max-epochs {n_epochs} \\
    --lr {learning_rate} \\
    {'--use-gpu' if use_gpu else ''} \\
    {'--early-stopping' if early_stopping else ''}

# 4. Cluster and visualize
python scripts/cluster_embed.py results/adata_trained.h5ad results/ --resolution 0.8

# 5. Differential expression
python scripts/differential_expression.py results/model results/adata_clustered.h5ad results/de.csv --groupby leiden"""

    st.code(commands, language="bash")

with tab3:
    st.header("Training Monitor (Demo)")

    np.random.seed(42)
    epochs = list(range(1, 101))
    train_loss = [800 * np.exp(-0.03 * e) + 200 + np.random.normal(0, 5) for e in epochs]
    val_loss = [820 * np.exp(-0.028 * e) + 210 + np.random.normal(0, 8) for e in epochs]

    loss_df = pd.DataFrame({"Epoch": epochs, "Train Loss (ELBO)": train_loss, "Validation Loss": val_loss})

    st.subheader("Training Loss (ELBO)")
    st.line_chart(loss_df.set_index("Epoch"))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Epoch", "100/200")
    col2.metric("Train ELBO", f"{train_loss[-1]:.1f}", f"{train_loss[-1] - train_loss[-2]:.1f}")
    col3.metric("Val ELBO", f"{val_loss[-1]:.1f}", f"{val_loss[-1] - val_loss[-2]:.1f}")
    col4.metric("Learning Rate", "1e-3")

    st.divider()
    st.subheader("Integration Metrics")

    metrics_col1, metrics_col2 = st.columns(2)
    with metrics_col1:
        st.metric("Silhouette Score (batch)", "0.82", "Good batch mixing")
        st.metric("ARI (cell type)", "0.91", "Strong cluster agreement")
    with metrics_col2:
        st.metric("NMI (cell type)", "0.88", "High mutual information")
        st.metric("kBET acceptance rate", "0.76", "Acceptable batch correction")

with tab4:
    st.header("Results Explorer (Demo)")

    st.subheader("UMAP Embedding")
    np.random.seed(123)
    n_cells = 500
    cell_types = np.random.choice(
        ["T cells", "B cells", "Monocytes", "NK cells", "Dendritic"],
        size=n_cells,
        p=[0.3, 0.2, 0.25, 0.15, 0.1],
    )

    centers = {
        "T cells": (2, 3),
        "B cells": (-3, -1),
        "Monocytes": (0, -3),
        "NK cells": (4, -2),
        "Dendritic": (-2, 3),
    }

    umap1, umap2 = [], []
    for ct in cell_types:
        cx, cy = centers[ct]
        umap1.append(cx + np.random.normal(0, 0.8))
        umap2.append(cy + np.random.normal(0, 0.8))

    umap_df = pd.DataFrame({"UMAP1": umap1, "UMAP2": umap2, "Cell Type": cell_types})
    st.scatter_chart(umap_df, x="UMAP1", y="UMAP2", color="Cell Type")

    st.divider()
    st.subheader("Differential Expression - Top Markers")

    de_data = {
        "Gene": ["CD3D", "CD79A", "LYZ", "NKG7", "FCER1A", "CD8A", "MS4A1", "S100A8", "GNLY", "HLA-DRA"],
        "Cluster": ["T cells", "B cells", "Monocytes", "NK cells", "Dendritic", "T cells", "B cells", "Monocytes", "NK cells", "Dendritic"],
        "Log2FC": [3.2, 4.1, 3.8, 2.9, 3.5, 2.7, 3.9, 3.3, 2.5, 3.1],
        "Adj. P-value": [1.2e-45, 3.4e-52, 8.7e-38, 2.1e-29, 5.6e-33, 4.3e-22, 1.8e-41, 7.2e-35, 9.1e-19, 3.3e-27],
        "Bayes Factor": [45.2, 52.1, 38.7, 29.3, 33.8, 22.1, 41.5, 35.2, 19.4, 27.6],
    }
    de_df = pd.DataFrame(de_data)
    st.dataframe(de_df, use_container_width=True, hide_index=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown(
    "This app provides an interactive interface for single-cell deep learning "
    "analysis using **scvi-tools**. Configure pipelines, monitor training, and "
    "explore results."
)
st.sidebar.markdown("### Key Requirements")
st.sidebar.markdown(
    "- Raw integer counts required\n"
    "- 2000-4000 HVGs recommended\n"
    "- Batch key must be specified for integration"
)
st.sidebar.markdown("### Resources")
st.sidebar.markdown("[scvi-tools Docs](https://docs.scvi-tools.org/)")
