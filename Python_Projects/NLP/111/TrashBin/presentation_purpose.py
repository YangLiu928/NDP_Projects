from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json
import numpy as np
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

training_set = joblib.load('training_set.pkl')
training_labels = joblib.load('training_labels.pkl')

SVM_Linear = Pipeline([
	('CountVectorizer',CountVectorizer(stop_words = 'english', ngram_range = (1,1))),
	('TfidfTransformer',TfidfTransformer()),
	('classifier',svm.LinearSVC())
	])

SVM_Linear = SVM_Linear.fit(training_set,training_labels)

joblib.dump(SVM_Linear,'linear_svm_classifier.pkl')


testing_set = ['Amends the Commodity Exchange Act to revise the requirement that the Commodity Futures Trading Commission (CFTC), before promulgating a regulation or issuing an order, consider the costs and benefits of the action. Requires the CFTC, through the Office of the Chief Economist, to: (1) assess the costs and benefits, both qualitative and quantitative, of an intended regulation; and (2) propose or adopt a regulation only on a reasoned determination that the benefits justify the costs. Lists additional mandatory considerations for the CFTC to evaluate in making a reasoned determination of the costs and the benefits, including the impact on market liquidity in the futures and swaps markets, as well as alternatives to direct regulation.',
	"""uccess and Opportunity through Quality Charter Schools Act - (Sec. 4) Revises subpart 1 (Charter School Program) of part B (Public Charter Schools) of title V (Promoting Informed Parental Choice and Innovative Programs) of the Elementary and Secondary Education Act of 1965.  (Sec. 5) Replaces the current charter school grant program with a program awarding grants to state entities (state educational agencies, state charter school boards, Governors, or charter school support organizations) and, through them, subgrants to charter school developers to open new charter schools and expand and replicate high-quality charter schools.  Requires grantees to use at least 7% of grant funds: (1) to provide technical assistance to subgrantees and authorized public chartering agencies, and (2) work with those agencies to improve the charter school authorization process. Prohibits grantees from reserving more than 3% of the grant funds for administrative costs. Directs the Comptroller General (GAO) to submit a report to the Secretary of Education and Congress, within three years of this Act's enactment, examining the appropriateness of that level of authorized funding for administrative costs.  Limits the duration of charter school grants and subgrants to no more than five years. Gives subgrantees no more than 18 months to plan and design their programs.   Prohibits the Secretary from awarding a charter school grant to a state entity if such award would result in more than one charter school grant being carried out in a state at the same time. Limits subgrantees to no more than one subgrant per charter school over a five-year period, unless the subgrantee demonstrates at least three years of improved educational results for students enrolled in the applicable charter school.  Requires the Secretary and each grantee to use a peer review process to review applications for charter school grants and subgrants.  Requires grantees to award subgrants in a manner that ensures, to the extent possible, that subgrants are distributed to different areas and assist charter schools representing a variety of educational approaches.  Permits the Secretary to waive certain statutory or regulatory requirements if the waiver is requested by a grant applicant and promotes the purpose of the Charter School program without tampering with what is definitionally required of charter schools. Directs the Secretary to give priority to grant applicants to the extent that they are from states that:  Directs the Secretary to give priority to grant applicants also to the extent that they:   (Sec. 6) Subsumes subpart 2 (Credit Enhancement Initiatives to Assist Charter School Facility Acquisition, Construction, and Renovation) of part B of title V under subpart 1. (Under subpart 2, the Secretary awards grants to public entities and private nonprofit entities to demonstrate innovative means of enhancing credit to finance the acquisition, construction, or renovation of charter schools.)  Requires the Secretary to award credit enhancement grants to applicants that have the highest-quality applications after considering the diversity of such applications. (Currently, the Secretary is required to award at least three grants, including at least one to a public entity, one to a private nonprofit entity, and one to a consortium of such entities, provided an application from each merits approval.)  Prohibits grant recipients from using more than 2.5% (currently, 0.25%) of their grant for administrative costs.  Revises the per-pupil facilities aid program (under which the Secretary makes competitive matching grants to states to provide per-pupil financing to charter schools) to allow states to: (1) partner with organizations to provide up to 50% of the state share of funding for the program; and (2) receive more than one program grant, so long as the amount of the grant funds provided to charter schools increases with each successive grant.  Allows states that are required by state law to provide charter schools with access to adequate facility space to qualify for a grant under the program even if they do not have a per-pupil facilities aid program for charter schools specified in state law, provided they agree to use the funds to develop such a program.  (Sec. 7) Directs the Secretary to conduct national activities that include:   (Sec. 8) Requires states and LEAs to ensure that a student's records are transferred as quickly as possible to a charter school or another public school when the student transfers from one such school to the other.  (Sec. 9) Allows charter schools to serve prekindergarten or postsecondary school students.  Defines a \"charter management organization\" as a nonprofit organization that manages a network of charter schools linked by centralized support, operations, and oversight.  (Sec. 10) Reauthorizes appropriations under subpart 1 through FY2020.  Directs the Secretary to use: (1) 12.5% of such funding for credit enhancement grants and the per-pupil facilities aid program, (2) up to 10% of such funding for the Secretary's national activities, and (3) the remaining funds for the charter school grant program."""]
test_labels = ['Finance and Financial Sector','Education']


predictions = SVM_Linear.predict(testing_set)
for prediction in predictions:
	print prediction





