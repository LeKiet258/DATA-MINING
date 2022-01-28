macro pr(t)
    :(debugging == true && println($t))
end
debugging = true

# taking the example data from wiki article http://en.wikipedia.org/wiki/Apriori_algorithm
articles = 1:4 #articles are represented as unique ids from 1 to 4
threshold = 3/8
transactions = {
{1,2,3,4}
{1,2,4}
{1,2}
{2,3,4}
{2,3}
{3,4}
{2,4}}

function apriori(transactions, threshold, articles)
    combination_max_size = length(articles)

    # combs_of_size[n] = all possible article combinations of size n
    combs_of_size = [Set(collect(combinations(articles, n))) for n in 1:combination_max_size]

    transactions_count = length(transactions)

    result = {}
    for n=1:combination_max_size
       @pr "------------------ looking at all combinations of size $n (combs_of_size[n]) -----------------"
       @pr "those are $(combs_of_size[n])\n"

        for comb in combs_of_size[n]
            # the percentage of transactions which the combination (comb) is a subset of 
            # (e.g.: [1,2] is subset of t3=[1,2] or of t2=[1,2,4])
            found_percentage = sum([issubset(comb,t) for t in transactions]) / transactions_count

            if found_percentage < threshold
                @pr "$comb is not in $(threshold*100)% of the transactions, thus "
                    "do not add it to result and possibly prune other bigger combos containing it."

                for j=n+1:combination_max_size
                    if length(combs_of_size[j]) > 0
                        @pr "\tpruning combs_of_size[$j] (= all combos of size $j)"
                        @pr "\t\tbefore: $(combs_of_size[j])"
                        filter!(c -> !issubset(comb, c), combs_of_size[j])
                        @pr "\t\tafter: $(combs_of_size[j])"
                    end
                end
            else
                @pr "$comb is in $(threshold*100)% of the transactions, thus adding it to result."
                push!(result, comb)
            end
        end
        @pr "\nfinished iteration for combinations of size $n, current result is:\n$result"
        
    end
    @show transactions
    @show result
end

apriori(transactions, threshold, articles)
