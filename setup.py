import setuptools

setuptools.setup(
    name="qspy",
    version="0.1.3",
    license='MIT',
    author="Gil's LAB",
    author_email="gils_lab@naver.com",
    description="python package for verifying quantative strategies",
    url="https://github.com/GilseungAhn/qspy.git",
    python_requires='>=3',
    packages=['qspy', 'qspy/analysis', 'qspy/datasets', 'qspy/utils'],
    install_requires=["numpy", "finance-datareader", "pandas"],
    package_data={
        'qspy': ['datasets/pickle_data/stock_price/*.pkl',
                 'datasets/pickle_data/finance_state/**/*.pkl',
                 'datasets/pickle_data/stock_list.xlsx',
                 'utils/Code_to_Name.pckl',
                 'utils/Name_to_Code.pckl']
    },
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)