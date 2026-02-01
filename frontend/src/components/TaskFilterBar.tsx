import React from 'react';

interface TaskFilterBarProps {
  completedFilter: string;
  priorityFilter: string;
  sortField: string;
  sortOrder: string;
  onCompletedChange: (value: string) => void;
  onPriorityChange: (value: string) => void;
  onSortFieldChange: (value: string) => void;
  onSortOrderChange: (value: string) => void;
  onClearFilters: () => void;
}

export default function TaskFilterBar({
  completedFilter,
  priorityFilter,
  sortField,
  sortOrder,
  onCompletedChange,
  onPriorityChange,
  onSortFieldChange,
  onSortOrderChange,
  onClearFilters
}: TaskFilterBarProps) {
  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8 mb-10 animate-fade-in border border-gray-200/60">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
        <div className="group">
          <label htmlFor="completed-filter" className="block text-sm font-semibold text-gray-700 mb-3 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-blue-100 to-indigo-100 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span className="text-gray-800">Status</span>
          </label>
          <select
            id="completed-filter"
            value={completedFilter}
            onChange={(e) => onCompletedChange(e.target.value)}
            className="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 group-hover:border-blue-300"
          >
            <option value="">All Tasks</option>
            <option value="true">Completed</option>
            <option value="false">Pending</option>
          </select>
        </div>

        <div className="group">
          <label htmlFor="priority-filter" className="block text-sm font-semibold text-gray-700 mb-3 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-yellow-100 to-orange-100 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 11l7-7 7 7M5 19l7-7 7 7" />
              </svg>
            </div>
            <span className="text-gray-800">Priority</span>
          </label>
          <select
            id="priority-filter"
            value={priorityFilter}
            onChange={(e) => onPriorityChange(e.target.value)}
            className="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-all duration-300 group-hover:border-yellow-300"
          >
            <option value="">All Priorities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="group">
          <label htmlFor="sort-field" className="block text-sm font-semibold text-gray-700 mb-3 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-purple-100 to-pink-100 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4" />
              </svg>
            </div>
            <span className="text-gray-800">Sort By</span>
          </label>
          <select
            id="sort-field"
            value={sortField}
            onChange={(e) => onSortFieldChange(e.target.value)}
            className="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300 group-hover:border-purple-300"
          >
            <option value="created_at">Date Created</option>
            <option value="due_date">Due Date</option>
            <option value="priority">Priority</option>
            <option value="title">Title</option>
          </select>
        </div>

        <div className="group">
          <label htmlFor="sort-order" className="block text-sm font-semibold text-gray-700 mb-3 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-green-100 to-teal-100 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
              </svg>
            </div>
            <span className="text-gray-800">Order</span>
          </label>
          <select
            id="sort-order"
            value={sortOrder}
            onChange={(e) => onSortOrderChange(e.target.value)}
            className="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300 group-hover:border-green-300"
          >
            <option value="desc">Descending</option>
            <option value="asc">Ascending</option>
          </select>
        </div>

        <div className="flex items-end">
          <button
            type="button"
            onClick={onClearFilters}
            className="w-full bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white font-semibold py-3 px-6 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl group relative overflow-hidden flex items-center justify-center gap-3"
          >
            <span className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform duration-500"></span>
            <span className="relative flex items-center gap-2 group-hover:gap-3 transition-all duration-300">
              <svg className="w-5 h-5 group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span>Clear Filters</span>
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}